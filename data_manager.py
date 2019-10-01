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
def search(search_phrase, cursor):
    cursor.execute(f"""
                        SELECT title FROM question WHERE title LIKE %{search_phrase}%;
                    """)
    search_phrase = cursor.fetchall()
    return search_phrase

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
def add_question(cursor,site_input):
    values=[common.get_id(),common.get_submission_time(),0,0,site_input[0],site_input[1],'']

    cursor.execute("""
                    INSERT INTO question(id,submission_time,view_number,vote_number,title,message,image)
                    VALUES(%(id)s,%(submission_time)s,%(view_number)s,%(vote_number)s,%(title)s,%(message)s,%(image)s)
                    """,
                   {'id': values[0],
                    'submission_time':values[1],
                    'view_number':values[2],
                    'vote_number':values[3],
                    'title':values[4],
                    'message':values[5],
                    'image':values[6]
                    })