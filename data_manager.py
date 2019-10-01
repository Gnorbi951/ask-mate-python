import time
import connection
import common


@connection.connection_handler
def get_least_questions(cursor):
    cursor.execute("""
                        SELECT title,message FROM question ORDER BY submission_time desc LIMIT 5;
                    """)
    table = cursor.fetchall()
    return table


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question;""")
    question_list = cursor.fetchall()
    return question_list


@connection.connection_handler
def get_comments_for_question(cursor, question_id):
    cursor.execute("""
                    SELECT message from comment
                    WHERE %(question_id)s = question_id;
                    """,
                   {'question_id': question_id})
    question_comments = cursor.fetchall()
    return question_comments


@connection.connection_handler
def get_answers_for_questions(cursor, question_id):
    cursor.execute("""
                    SELECT message FROM answer
                    WHERE question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    question_answers = cursor.fetchall()
    return question_answers


@connection.connection_handler
def add_question(cursor, site_input):
    title, message = 0, 1
    new_id = common.get_id()
    current_id = new_id[0].get('max')
    current_id += 1
    sub_time = common.get_submission_time()
    values = [current_id, sub_time, 0, 0, site_input[title], site_input[message], 'No image']

    cursor.execute("""
                    INSERT INTO question(id,submission_time,view_number,vote_number,title,message,image)
                    VALUES(%(id)s, %(sub_time)s, %(view_number)s,
                            %(vote_number)s, %(title)s, %(message)s, %(image)s); 
                    """,
                   {'id': values[0],
                    'sub_time': values[1],
                    'view_number': values[2],
                    'vote_number': values[3],
                    'title': values[4],
                    'message': values[5],
                    'image': values[6]})

#outsorce this
'''
def get_submission_time():
    return time.time()

def get_id():#sql_table
    cursor.execute("""
                    SELECT id FROM question ORDER BY desc LIMIT 1
    
                    """)
    id=cursor.fetchall()
    return id+1
'''
#outsorce this
