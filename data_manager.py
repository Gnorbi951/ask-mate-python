import connection
import common


@connection.connection_handler
def get_least_questions(cursor):
    cursor.execute("""
                        SELECT title,message FROM question
                        ORDER BY submission_time DESC 
                        LIMIT 5;
                    """)
    table = cursor.fetchall()
    return table


@connection.connection_handler
def search(cursor, search_phrase):
    search_phrase = '%' + search_phrase + '%'
    cursor.execute("""
                        SELECT title FROM question
                        WHERE title LIKE %(search_phrase)s; 
                    """,
                   {'search_phrase': search_phrase})
    search_phrase_title = cursor.fetchall()
    cursor.execute("""
                        SELECT message FROM question
                        WHERE message LIKE %(search_phrase)s; 
                    """,
                   {'search_phrase': search_phrase})
    search_phrase_message = cursor.fetchall()
    cursor.execute("""
                            SELECT message FROM answer
                            WHERE message LIKE %(search_phrase)s; 
                        """,
                   {'search_phrase': search_phrase})
    search_phrase_answer = cursor.fetchall()
    return search_phrase_title, search_phrase_message, search_phrase_answer


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute("""
                    SELECT COALESCE(user_name, 'Guest') AS name_of_user, submission_time,
                        question.message, question.vote_number, question.id, question.title
                    FROM question
                    LEFT JOIN users
                        ON question.user_id = users.id
                    ORDER BY submission_time DESC""")
    question_list = cursor.fetchall()
    return question_list


@connection.connection_handler
def get_comments_for_question(cursor, question_id):
    cursor.execute("""
                    SELECT id, message FROM comment
                    WHERE %(question_id)s = question_id
                    ORDER BY submission_time;
                    """,
                   {'question_id': question_id})
    question_comments = cursor.fetchall()
    return question_comments


@connection.connection_handler
def get_comments_for_answer(cursor, answer_id):
    cursor.execute("""
                    SELECT a.message, c.message AS comment_message, a.id, c.id AS comment_id
                     FROM answer AS a 
                    INNER JOIN comment c ON a.id=c.answer_id
                    WHERE %(answer_id)s = answer_id
                    ORDER BY c.submission_time;
                    """,
                   {'answer_id': answer_id})
    answer_comment = cursor.fetchall()
    return answer_comment


@connection.connection_handler
def get_answers_for_questions(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id = %(question_id)s
                    ORDER BY submission_time;
                    """,
                   {'question_id': question_id})
    question_answers = cursor.fetchall()
    return question_answers


@connection.connection_handler
def get_answer_id(cursor, answer_message):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE message = %(answer_message)s;
                    """,
                   {'answer_message': answer_message})
    answer_details = cursor.fetchall()
    return answer_details


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
                   {'answer_id': answer_id})
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
def get_question_id_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT q.id FROM question AS q
                    JOIN answer a on q.id = a.question_id
                    WHERE a.id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id})
    question_id = cursor.fetchall()
    return question_id


@connection.connection_handler
def add_question(cursor, site_input):
    values = [common.get_id('question'), common.get_submission_time(), 0, 0, site_input[0], site_input[1], '',site_input[2]]

    cursor.execute("""
                    INSERT INTO question(id, submission_time, view_number, vote_number, 
                                         title, message, image,user_id)
                    VALUES(%(id)s, %(submission_time)s, %(view_number)s, 
                           %(vote_number)s, %(title)s, %(message)s, %(image)s,%(user_id)s)
                    """,
                   {'id': values[0],
                    'submission_time': values[1],
                    'view_number': values[2],
                    'vote_number': values[3],
                    'title': values[4],
                    'message': values[5],
                    'image': values[6],
                    'user_id':values[7]
                    })


@connection.connection_handler
def edit_question(cursor, site_input):
    cursor.execute("""
                    UPDATE question
                    SET message = %(message)s, title = %(title)s
                    WHERE id = %(question_id)s;
                    """,
                   {
                        'message' : site_input[1],
                        'title' : site_input[0],
                        'question_id' : site_input[2]})



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
                       {'question_id': question_id,
                        'answer_id': answer_id,
                        'message': message,
                        'submission_time': submission_time,
                        'edited_count': edited_count})


@connection.connection_handler
def edit_answer(cursor, site_input):
    cursor.execute("""
                    UPDATE answer SET message = %(message)s 
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id': site_input[1],
                    'message': site_input[0]})


@connection.connection_handler
def add_user(cursor, inputs):
    """
    :param cursor: conncetion handler
    :param inputs: Accepts a list, [0] is user_name, [1] is HASHED password
    :return: writes in the table
    """
    username, password = 0, 1
    cursor.execute("""
                    INSERT INTO users (user_name, password)
                        VALUES (%(user)s, %(pw)s);
                        """,
                   {'user': inputs[username],
                    'pw': inputs[password]})


@connection.connection_handler
def get_existing_users(cursor):
    cursor.execute("""
                    SELECT user_name, password FROM users ;
                        """)
    existing_users = cursor.fetchall()
    return existing_users



@connection.connection_handler
def list_users(cursor):
    cursor.execute("""
                    SELECT id, user_name, registration_date, status
                    FROM users""")
    users = cursor.fetchall()
    return users


@connection.connection_handler
def get_user_activities(cursor, user_id):
    cursor.execute("""
                    SELECT a.message AS ans_message, c.message AS com_message,
                    q.title, u.user_name, q.id  FROM users AS u 
                    JOIN answer a on u.id = a.user_id
                    JOIN question q on u.id = q.user_id
                    JOIN comment c on u.id = c.user_id
                    WHERE u.id = %(user_id)s;
                    """,
                   {'user_id':user_id})
    user_activities = cursor.fetchall()
    return user_activities


@connection.connection_handler
def vote_up(cursor, question_id):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = vote_number + 1
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id':question_id})


@connection.connection_handler
def vote_down(cursor, question_id):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = vote_number - 1
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id':question_id})


@connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id':question_id})


@connection.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""
                    UPDATE answer
                    SET message = %(message)s
                    WHERE id = %(answer_id)s
                    """,
                   {'answer_id':answer_id,
                    'message':'[deleted]'})


@connection.connection_handler
def delete_comment(cursor, comment_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE id = %(comment_id)s
                    """,
                   {'comment_id':comment_id})


@connection.connection_handler
def get_answer_id_by_comment_id(cursor, comment_id):
    cursor.execute("""
                    SELECT c.answer_id FROM comment c
                    WHERE c.id = %(comment_id)s;
                    """,
                   {'comment_id':comment_id})
    answer_id = cursor.fetchall()
    return answer_id


@connection.connection_handler
def get_question_id_by_comment_id(cursor, comment_id):
    cursor.execute("""
                    SELECT c.question_id FROM comment c
                    WHERE c.id = %(comment_id)s;
                    """,
                   {'comment_id' : comment_id})
    question_id = cursor.fetchall()
    return question_id


@connection.connection_handler
def vote_up_answer(cursor, answer_id):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = vote_number + 1
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id':answer_id})


@connection.connection_handler
def vote_down_answer(cursor, answer_id):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = vote_number - 1
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id':answer_id})


@connection.connection_handler
def get_id_by_name(cursor, name):
    cursor.execute("""
                    SELECT id FROM users
                    WHERE user_name = %(name)s;
                    """,
                   {'name': name})
    user_id = cursor.fetchall()
    return user_id

