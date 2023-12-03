import flask
from flask import Flask, render_template, request


from data_handler import answer_data_handler as adh, question_data_handler as qdh, \
    comments_tags_data_handler as cdh

app = Flask(__name__)


@app.route("/")
def starting_page():
    questions = qdh.get_five_most_recent_questions()
    return render_template('main_page.html', questions=questions)


@app.route("/list", methods=['POST', 'GET'])
def question_list():
    sort_value = request.form.get("sort_value")
    sort_direction = request.form.get("sort_direction")
    if sort_value is None:
        sort_value = "id"
        sort_direction = """ASC"""
    questions = qdh.get_all_questions(sort_value, sort_direction)
    return render_template("list.html", questions=questions)


@app.route('/question/<question_id>')
def question_display(question_id):
    try:
        answer_id = adh.get_answer_by_question_id(question_id)['id']
    except TypeError:
        answer_id = 0
    questions = qdh.get_question_by_id(question_id)
    answers = adh.get_all_answers(question_id)
    comments = cdh.get_comments_to_question(question_id)
    return render_template("question_display.html", question_id=question_id, question=questions, answers=answers,
                           comments=comments, answer_id=answer_id)


@app.route("/add-question", methods=['POST', 'GET'])
def add_question():
    if request.method == "GET":
        return render_template('add_question.html')
    if request.method == "POST":
        title = request.form.get("title")
        message = request.form.get("message")
        image = request.files.get("filename")
        filename = qdh.add_file(image)
        question = qdh.save_new_question(title, message, filename)
        return flask.redirect(f"/question/{question['id']}")


@app.route("/question/<question_id>/new-answer", methods=['POST', 'GET'])
def add_answer(question_id):
    if request.method == "GET":
        return render_template('add_answer.html', question_id=question_id)
    if request.method == "POST":
        answer = {'vote_number': 0, 'question_id': question_id,
                  'message': request.form.get('message'), 'image': None}
        adh.save_new_answer(answer)
        return flask.redirect(f"/question/{question_id}")


@app.route('/question/<question_id>/delete', methods=['POST', 'GET'])
def delete_questions(question_id):
    if request.method == 'GET':
        return flask.render_template('delete_question.html')
    if request.method == 'POST':
        qdh.delete_question(question_id)
        return flask.redirect("/list")


@app.route("/answer/<answer_id>/delete", methods=['POST', 'GET'])
def delete_answer(answer_id):
    if request.method == 'GET':
        return render_template('delete_answer.html', answer_id=answer_id)
    if request.method == 'POST':
        answer = adh.get_answer_by_id(answer_id)
        adh.delete_answer(answer_id)
        return flask.redirect(f"/question/{answer['question_id']}")


@app.route('/question/<question_id>/vote-up')
def vote_question_up(question_id):
    vote = 1
    qdh.vote_question(question_id, vote)
    return flask.redirect(f"/question/{question_id}")


@app.route('/question/<question_id>/vote-down')
def vote_question_down(question_id):
    vote = -1
    qdh.vote_question(question_id, vote)
    return flask.redirect(f"/question/{question_id}")


@app.route('/answer/<answer_id>/vote-up')
def vote_answer_up(answer_id):
    vote = 1
    adh.vote_answer(answer_id, vote)
    question = qdh.get_question_id_by_answer_id(answer_id)
    return flask.redirect(f"/question/{question['question_id']}")


@app.route('/answer/<answer_id>/vote-down')
def vote_answer_down(answer_id):
    vote = -1
    adh.vote_answer(answer_id, vote)
    question = qdh.get_question_id_by_answer_id(answer_id)
    return flask.redirect(f"/question/{question['question_id']}")


@app.route('/question/<question_id>/edit', methods=['POST', 'GET'])
def edit_question(question_id):
    if request.method == 'GET':
        question = qdh.get_question_by_id(question_id)
        return render_template("edit_question.html", question=question)
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        qdh.edit_question(title, message, question_id)
        return flask.redirect(f"/question/{question_id}")


@app.route('/question/<question_id>/new-comment', methods=['POST', 'GET'])
def new_question_comment(question_id):
    if request.method == "GET":
        return render_template('add_comment.html', question_id=question_id)
    if request.method == 'POST':
        comment = {'question_id': question_id, 'answer_id': None, 'message': request.form.get('message'),
                   'edited_count': 0}
        cdh.add_comments(comment)
        return flask.redirect(f"/question/{question_id}")


@app.route('/answer/<answer_id>/new-comment', methods=['POST', 'GET'])
def add_comment_to_answer_form(answer_id):
    if request.method == 'GET':
        return render_template('add_comment.html', answer_id=answer_id)
    if request.method == 'POST':
        answer = adh.get_answer_by_id(answer_id)
        comment = {'question_id': None, 'answer_id': answer_id, 'message': request.form.get('message'),
                   'edited_count': 0}
        cdh.add_comments(comment)
        return flask.redirect(f"/question/{answer['question_id']})")


@app.route('/comments/<comment_id>/edit', methods=['POST', 'GET'])
def edit_comment(comment_id):
    if request.method == 'GET':
        comment = cdh.get_comment_by_comment_id(comment_id)
        for com in comment:
            com = dict(com)
        return render_template('edit_comment.html', comment=com)
    if request.method == 'POST':
        message = request.form.get('message')
        cdh.edit_comment(message, comment_id)
        count = 1
        cdh.update_edit_counts(comment_id, count)
        question = cdh.get_question_id_by_comment_id(comment_id)
        if question is not None:
            return flask.redirect(f"/question/{question['question_id']}")
        else:
            question = cdh.direct_to_question()
            return flask.redirect(f"/question/{question['question_id']}")


@app.route('/comments/<comment_id>/delete')
def delete_comment(comment_id):
    question_id = cdh.get_question_id_by_comment_id(comment_id)['question_id']
    cdh.delete_comment(comment_id)
    return flask.redirect(f"/question/{question_id}")


@app.route('/question/<question_id>/new-tag', methods=['POST', 'GET'])
def render_tags(question_id):
    if request.method == 'GET':
        tags = cdh.get_all_tags()
        return render_template("tags.html", tags=tags, question_id=question_id)
    if request.method == 'POST':
        new_tag = request.form.get('new-tag')
        tag_id = cdh.save_new_tag(new_tag)
        cdh.save_tag_to_question_tag(question_id, tag_id['id'])
        return flask.redirect(f"/question/{question_id}")


@app.route('/question/<question_id>/<tag_id>')
def save_tag_from_existing_tags(question_id, tag_id):
    cdh.save_existing_tag_to_question(question_id, tag_id)
    return flask.redirect(f"/question/{question_id}")


@app.route('/question/<question_id>/view-up')
def increase_views(question_id):
    qdh.increase_view_number(question_id)
    return flask.redirect(f"/question/{question_id}")


@app.route('/question/<question_id>/<tag_id>/delete_tag')
def delete_tag(question_id, tag_id):
    cdh.delete_tag_from_tag(tag_id)
    return flask.redirect(f"/question/{question_id}")


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    if request.method == 'GET':
        answer = adh.get_answer_by_id(answer_id)
        return render_template('edit_answer.html', answer=answer)
    if request.method == 'POST':
        message = request.form.get('message')
        question = adh.edit_answer(message, answer_id)
        return flask.redirect(f"/question/{question['question_id']}")


@app.route('/question/<question_id>/answer/<answer_id>')
def see_answer_comments(answer_id, question_id):
    question = qdh.get_question_by_id(question_id)
    answer = adh.get_commented_answer(question_id, answer_id)
    comments = cdh.get_comments_to_question(question_id)
    answer_comments = cdh.get_comments_to_answer()
    return render_template('answer_display.html', answer_id=answer_id, question_id=question_id, question=question,
                           answer=answer, comments=comments, answer_comments=answer_comments)


if __name__ == "__main__":
    app.run()
