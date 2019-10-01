import csv
import time
import connection


@connection.connection_handler
def get_least_questions(cursor):
    cursor.execute("""
                        SELECT title,message FROM question ORDER BY submission_time desc LIMIT 5;
                    """)
    table=cursor.fetchall()
    return table
'''
@connection.connection_handler
def edit_answers(cursor,<answer_id>,new_title,new_message):
    cursor.execute("""
    UPDATE answer SET title=new_title, message=new_message WHERE id=;
                    """)


@connection.connection_handler
def add_answer(cursor,id,submission_time,vote_number,question_id,message,image):

    cursor.execute("""
                       INSERT INTO answer(id,submission_time,vote_number,question_id,message,image) 
                       VALUES(id,submission_time,vote_number,question_id,message,image);
                    """)


'''