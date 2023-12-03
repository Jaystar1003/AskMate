import os
import time
import database_common


dir_path = os.path.dirname(os.path.realpath(__file__))


@database_common.connection_handler
def get_all_answers(cursor, question_id):
    query = """ SELECT * 
                FROM answer 
                WHERE question_id = (%(question_id)s) 
                ORDER BY vote_number DESC"""
    answer = {'question_id': question_id}
    cursor.execute(query, answer)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_by_question_id(cursor, question_id):
    query = """
        SELECT *
        FROM answer
        WHERE question_id = %(question_id)s
        """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchone()


@database_common.connection_handler
def get_answer_by_id(cursor, answer_id):
    query = """
        SELECT *
        FROM answer
        WHERE id = %(answer_id)s
        """
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


@database_common.connection_handler
def save_new_answer(cursor, new_answer):
    sub_time = time.strftime("%Y-%m-%d %H:%M")
    query = """ 
            INSERT INTO answer(submission_time, vote_number, question_id, message, image) 
            VALUES (%(submission_time)s,%(vote_number)s,%(question_id)s,%(message)s,%(image)s )"""
    new_answers = {'submission_time': sub_time, 'vote_number': new_answer['vote_number'],
                   'question_id': new_answer['question_id'], 'message': new_answer['message'], 'image': new_answer['image']}
    cursor.execute(query, new_answers)


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    query = """DELETE FROM answer 
               WHERE id= %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})


@database_common.connection_handler
def vote_answer(cursor, answer_id, vote):
    query = """
        UPDATE answer
        SET vote_number = vote_number + %(vote)s
        WHERE id = %(answer_id)s
            """
    return cursor.execute(query, {"answer_id": answer_id, 'vote': vote})


@database_common.connection_handler
def edit_answer(cursor,  message, question_id):
    query = f""" 
                UPDATE answer
                SET message = '{message}'
                WHERE id = {question_id}   
                RETURNING question_id         
                """
    cursor.execute(query)
    return cursor.fetchone()


def get_commented_answer(question_id, answer_id):
    answers = get_all_answers(question_id)
    for answer in answers:
        if answer['id'] == int(answer_id):
            commented_answer = answer
            return commented_answer
    return None
