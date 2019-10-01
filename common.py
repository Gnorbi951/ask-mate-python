import datetime
import connection


def get_submission_time():

    return datetime.date.today()


@connection.connection_handler
def get_id(cursor, table):  # sql_table
    if table == 'question':
        cursor.execute("""
                        SELECT MAX(id) FROM question;
    
                        """)
    elif table == 'comment':
        cursor.execute("""
                        SELECT MAX(id) FROM comment;

                                """)
    elif table == 'answer':
        cursor.execute("""
                        SELECT MAX(id) FROM answer;

                                        """)

    max_id = cursor.fetchall()
    return max_id[0].get('max')+1
