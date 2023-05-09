import psycopg2

from config import dbname, user, password, host

conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
cursor = conn.cursor()

def get_answers(question_id):
    cursor.execute(f"""
                   SELECT answer_id, content, correctness, user_id
                   FROM answers
                   WHERE question_id = {question_id}
                   """)
    temp = cursor.fetchall()
    answers = [{"id":answer[0], "content": answer[1], 
                "correctness": answer[2], "user_id": answer[3]} for answer in temp]
    return answers