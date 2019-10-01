import connection

@connection.connection_handler
def get_least_questions(cursor):
    cursor.execute("""
                        SELECT title,message FROM question ORDER BY submission_time desc LIMIT 5;
                    """)
    table = cursor.fetchall()
    return table


@connection.connection_handler
def search(cursor, search_phrase):
    search_phrase = '%' + search_phrase + '%'
    cursor.execute("""
                        SELECT title FROM question
                        WHERE title LIKE %(search_phrase)s 
                        OR message LIKE %(search_phrase)s;
                    """, #We need also search in answers
                   {'search_phrase': search_phrase})
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