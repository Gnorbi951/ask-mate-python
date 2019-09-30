import connection

@connection.connection_handler
def test(cursor):
    cursor.execute("""
                    SELECT * FROM answer;""")
    answers = cursor.fetchall()
    return answers
