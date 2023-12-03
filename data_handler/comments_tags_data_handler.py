import os
import time
import database_common


dir_path = os.path.dirname(os.path.realpath(__file__))


@database_common.connection_handler
def get_comments_to_question(cursor, question_id):
    query = """ SELECT * 
                FROM comment 
                WHERE question_id = (%(question_id)s) """
    comment = {'question_id': question_id}
    cursor.execute(query, comment)
    return cursor.fetchall()


@database_common.connection_handler
def add_comments(cursor, new_comment):
    sub_time = time.strftime("%Y-%m-%d %H:%M")
    query = """ INSERT INTO comment(question_id, answer_id, message, submission_time, edited_count) 
                VALUES (%(question_id)s,%(answer_id)s,%(message)s,%(submission_time)s,%(edited_count)s )"""
    new_comments = {'question_id': new_comment['question_id'],'answer_id': new_comment['answer_id'],
                    'message': new_comment['message'], 'submission_time': sub_time,
                    'edited_count': new_comment['edited_count']}
    cursor.execute(query, new_comments)


@database_common.connection_handler
def get_comments_to_answer(cursor):
    query = """ 
            SELECT comment.message, comment.answer_id, comment.id, comment.edited_count, comment.question_id 
            FROM comment 
            INNER JOIN answer ON comment.answer_id = answer.id
     """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_by_comment_id(cursor, comment_id):
    query = """ 
            SELECT message, id 
            FROM comment 
            WHERE id= %(comment_id)s"""
    cursor.execute(query, {'comment_id': comment_id})
    return cursor.fetchall()


@database_common.connection_handler
def delete_comment(cursor, comment_id):
    query = f"""
        DELETE FROM comment
        WHERE id = '{comment_id}'
        """
    return cursor.execute(query)


@database_common.connection_handler
def delete_comment_to_answer(cursor,answer_id):
    query = """
            DELETE FROM comment 
            WHERE answer_id= %(answer_id)s"""
    cursor.execute(query, {"answer_id": answer_id})


@database_common.connection_handler
def edit_comment(cursor, message, comment_id):
    query = f""" 
            UPDATE comment 
            SET message = '{message}' WHERE id = {comment_id} """
    cursor.execute(query)


@database_common.connection_handler
def get_question_id_by_comment_id(cursor, comment_id):
    query = """
        SELECT question_id
        FROM comment
        WHERE id = %(comment_id)s"""
    cursor.execute(query, {'comment_id': comment_id})
    return cursor.fetchone()


@database_common.connection_handler
def direct_to_question(cursor):
    query = """ 
            SELECT answer.question_id  
            FROM answer 
            INNER JOIN comment ON answer.id= comment.answer_id """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def update_edit_counts(cursor, comment_id, count):
    query = """ 
            UPDATE comment 
            SET edited_count = edited_count + %(count)s 
            WHERE id = %(comment_id)s """
    return cursor.execute(query, {'comment_id': comment_id, 'count': count})
