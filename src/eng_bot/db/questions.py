import psycopg2

from config import dbname, user, password, host

conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
cursor = conn.cursor()

def get_question_types():
    cursor.execute(f"SELECT type_id, name FROM question_types")
    
    question_types = [{"id": type_id, "name": name} for type_id, name in cursor.fetchall()]
    return question_types

def get_content(question_id):
    cursor.execute(f"SELECT content FROM questions WHERE question_id = {question_id}")
    
    question_name = cursor.fetchone()[0]
    return question_name

def get_test_id(question_id):
    cursor.execute(f"SELECT test_id FROM questions WHERE question_id = {question_id}")
    
    test_id = cursor.fetchone()[0]
    return test_id

def get_questions(test_id):
    cursor.execute(f"""
                   SELECT question_id, content, price, type_id, user_id
                   FROM questions
                   WHERE test_id = {test_id};
                   """)
    temp = cursor.fetchall()
    questions = [{"id": question[0], "content": question[1], 
                  "price": question[2], "type_id": question[3], 
                  "user_id": question[4]} for question in temp]
    return questions

def is_answer_visibility(type_id):
    cursor.execute(f"""
                   SELECT answer_visibility
                   FROM question_types
                   WHERE type_id = {type_id}
                   """)
    answer_visibility = cursor.fetchone()[0]
    return answer_visibility