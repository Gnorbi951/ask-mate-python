import time
import connection


def get_submission_time():
    current_time = time.time()
    return int(current_time)


@connection.connection_handler
def get_id(cursor):  # sql_table
    cursor.execute("""
                    SELECT MAX(id) FROM question;

                    """)
    max_id = cursor.fetchall()
    return max_id
