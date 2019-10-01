import csv
import time
import connection

@connection.connection_handler
def get_least_questions(cursor):
    cursor.execute("""
                        SELECT title,message FROM question ORDER BY submission_time desc LIMIT 5;
                    """)
    table = cursor.fetchall()
    return table


@connection.connection_handler
def search(search_phrase, cursor):
    cursor.execute("""
                        SELECT title, message FROM question WHERE title LIKE %(search_phrase)s
                    """,
                   {'search_phrase':search_phrase})
    result = cursor.fetchall()
    return result