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

def get_last_answers(user_id, amount):
    cursor.execute(f"""
                   SELECT user_id, question_id, correctness, date, answer_content
                   FROM test_answers
                   WHERE user_id = {user_id}
                   ORDER BY date DESC
                   LIMIT {amount};
                   """)
    
    temp = cursor.fetchall()
    answers = [{'user_id': answer[0], 'question_id': answer[1], 
                                    'correctness': answer[2], 'date': answer[3], 
                                    'answer_content': answer[4]} for answer in temp]
    return answers