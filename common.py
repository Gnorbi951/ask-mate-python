import datetime
import connection


def get_submission_time():

    return datetime.date.today()


@connection.connection_handler
def get_id(cursor):  # sql_table
    cursor.execute("""
                    SELECT MAX(id) FROM question;

                    """)
    max_id = cursor.fetchall()
    #print('max_id:'+(max_id.get('max')+1))
    return max_id[0].get('max')+1
