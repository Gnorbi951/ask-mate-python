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
def search(cursor, search_phrase):
    search_phrase = '%' + search_phrase + '%'
    cursor.execute("""
                        SELECT title FROM question
                        WHERE title LIKE %(search_phrase)s 
                        OR message LIKE %(search_phrase)s;
                    """,  # We need also search in answers
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
                    SELECT message FROM comment
                    WHERE %(question_id)s = question_id;
                    """,
                   {'question_id': question_id})
    question_comments = cursor.fetchall()
    return question_comments


@connection.connection_handler
def get_comments_for_answer(cursor, answer_id, answer_message):
    cursor.execute("""
                    SELECT comment.message, answer.id, answer.message FROM answer
                    INNER JOIN comment ON answer.id=comment.answer_id
                    WHERE %(answer_id)s = answer_id;
                    """,
                   {'answer_id': answer_id})
    print(answer_message)
    answer_comment = cursor.fetchall()
    return answer_comment

@connection.connection_handler
def get_answer_message(cursor, question_id):
    cursor.execute("""
                    SELECT message FROM answer
                    WHERE question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    answer_message = cursor.fetchall()
    return answer_message



@connection.connection_handler
def get_answers_for_questions(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    question_answers = cursor.fetchall()
    return question_answers


@connection.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    question_details = cursor.fetchall()
    return question_details


@connection.connection_handler
def get_answer_by_id(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id' : answer_id})
    answer_details = cursor.fetchall()
    return answer_details


@connection.connection_handler
def get_answer_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id = %(question_id)s;
                    """,
                   {'question_id' : question_id})
    answer_details = cursor.fetchall()
    return answer_details


@connection.connection_handler
def add_question(cursor, site_input):
    values = [common.get_id('question'), common.get_submission_time(), 0, 0, site_input[0], site_input[1], '']

    cursor.execute("""
                    INSERT INTO question(id, submission_time, view_number, vote_number, 
                                         title, message, image)
                    VALUES(%(id)s, %(submission_time)s, %(view_number)s, 
                           %(vote_number)s, %(title)s, %(message)s, %(image)s)
                    """,
                   {'id': values[0],
                    'submission_time': values[1],
                    'view_number': values[2],
                    'vote_number': values[3],
                    'title': values[4],
                    'message': values[5],
                    'image': values[6]
                    })


@connection.connection_handler
def add_answer(cursor, site_input, question_id):
    values = [common.get_submission_time(), 0, question_id[0], site_input, '']

    cursor.execute("""
                      INSERT INTO answer(submission_time,vote_number,question_id,message,image)
                      VALUES (%(submission_time)s,%(vote_number)s,%(question_id)s,%(message)s,%(image)s)
                    """,
                   {
                       'submission_time': values[0],
                       'vote_number': values[1],
                       'question_id': values[2],
                       'message': values[3],
                       'image': values[4]})


@connection.connection_handler
def add_comment(cursor, server_input):
    id_, comment, instance = 0, 1, 2
    if server_input[instance] == 'question':
        question_id = server_input[id_]
        answer_id = None
        message = server_input[comment]
        submission_time = common.get_submission_time()
        edited_count = None

        cursor.execute("""
                            INSERT INTO comment(question_id, answer_id, message,
                                                submission_time, edited_count)
                            VALUES(%(question_id)s, %(answer_id)s, %(message)s,
                                   %(submission_time)s, %(edited_count)s);
                                   """,
                       {'question_id': question_id,
                        'answer_id': answer_id,
                        'message': message,
                        'submission_time': submission_time,
                        'edited_count': edited_count})
    else:
        answer_id = server_input[id_]
        question_id = None
        submission_time = common.get_submission_time()
        message = server_input[comment]
        edited_count = None
        cursor.execute("""
                            INSERT INTO comment(question_id, answer_id, message,
                                                submission_time, edited_count)
                            VALUES(%(question_id)s, %(answer_id)s, %(message)s,
                                   %(submission_time)s, %(edited_count)s);
                                   """,
                       {'question_id':question_id,
                        'answer_id':answer_id,
                        'message':message,
                        'submission_time':submission_time,
                        'edited_count':edited_count})

