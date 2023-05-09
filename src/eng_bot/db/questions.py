import psycopg2

from config import dbname, user, password, host

conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
cursor = conn.cursor()

def get_question_types():
    cursor.execute(f"SELECT type_id, name FROM question_types")
    
    question_types = [{"id": type_id, "name": name} for type_id, name in cursor.fetchall()]
    return question_types

def get_questions(test_id):
    cursor.execute(f"""
                   SELECT question_id, content, price, type, user_id
                   FROM questions
                   WHERE test_id = {test_id};
                   """)
    temp = cursor.fetchall()
    questions = [{"id": question[0], "content": question[1], 
                  "price": question[2], "type": question[3], 
                  "user_id": question[4]} for question in temp]
    return questions