import os
import time
import database_common


dir_path = os.path.dirname(os.path.realpath(__file__))


@database_common.connection_handler
def get_all_questions(cursor, sort_value, sort_direction):
    query = f"""
        SELECT *
        FROM question
        ORDER BY {sort_value} {sort_direction}"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    query = """
        SELECT *
        FROM question
        WHERE id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchone()


@database_common.connection_handler
def save_new_question(cursor, title, message, image):
    submission_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = f"""
                INSERT INTO question 
                VALUES (DEFAULT, '{submission_time}', 0, 0, '{title}', '{message}', '{image}' )   
                RETURNING id;    
            """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def delete_question(cursor, question_id):
    query = """ DELETE FROM answer WHERE question_id= %(question_id)s;
                DELETE FROM question_tag WHERE question_id= %(question_id)s;
                DELETE FROM question WHERE id= %(question_id)s"""
    cursor.execute(query, {"question_id": question_id})


@database_common.connection_handler
def vote_question(cursor, question_id, vote):
    query = """
        UPDATE question
        SET vote_number = vote_number + %(vote)s
        WHERE id = %(question_id)s
            """
    return cursor.execute(query, {"question_id": question_id, 'vote': vote})


@database_common.connection_handler
def edit_question(cursor, title, message, question_id):
    query = f""" 
                UPDATE question 
                SET title = '{title}',
                    message = '{message}'
                WHERE id = {question_id}
                """
    return cursor.execute(query)


def add_file(file):
    try:
        filename = os.path.basename(file.filename)
        file_name = os.path.join(dir_path[:-12], "images", filename)
        open(file_name, 'wb').write(file.read())
    except:
        filename = 'BLANK_ICON.png'
    return filename


@database_common.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    query = """
        SELECT question_id
        FROM answer
        WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


@database_common.connection_handler
def get_five_most_recent_questions(cursor):
    query = """
        SELECT id, submission_time, view_number, vote_number, title, message, image
        FROM question
        ORDER BY submission_time DESC
        LIMIT 5"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def increase_view_number(cursor, question_id):
    query = """
        UPDATE question
        SET view_number = view_number+ 1
        WHERE id = %(question_id)s
            """
    cursor.execute(query, {"question_id": question_id})
