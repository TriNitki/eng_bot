import psycopg2
from datetime import datetime

from config import dbname, user, password, host

conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
cursor = conn.cursor()

def get_tests(topic_id):
    cursor.execute(f"SELECT name, test_id, user_id FROM tests WHERE topic_id = {topic_id}")
    tests = cursor.fetchall()
    result = [{'name': test[0], 'id': test[1], 'user_id': test[2]} for test in tests]
    return result

def get_test(test_id):
    cursor.execute(f"SELECT name, user_id FROM tests WHERE test_id = {test_id}")
    temp = cursor.fetchone()
    test = {"name": temp[0], "user_id": temp[1]}
    return test

def add(user_id, topic_id, test):
    cursor.execute(f"INSERT INTO tests(user_id, topic_id, name) VALUES({user_id}, {topic_id}, '{test.name}')")
    conn.commit()
    
    cursor.execute(f"SELECT test_id FROM tests WHERE name = '{test.name}'")
    test_id = cursor.fetchone()[0]
    for question in test.questions:
        cursor.execute(f"""
                       INSERT INTO questions(content, price, test_id, type, user_id) 
                       VALUES('{question.content}', {question.price}, {test_id}, '{question.type}', {user_id})
                       """)
        conn.commit()
        
        cursor.execute(f"SELECT question_id FROM questions WHERE content = '{question.content}'")
        question_id = cursor.fetchone()[0]
        for answer in question.answers:
            cursor.execute(f"""
                           INSERT INTO answers(content, correctness, question_id, user_id) 
                           VALUES('{answer.content}', {answer.correctness}, {question_id}, {user_id})
                           """)
    
    conn.commit()
    
def get_highest_score(user_id, test_id):
    cursor.execute(f"""
                   SELECT MAX(score)
                   FROM test_results
                   WHERE test_id = {test_id} AND user_id = {user_id};
                   """)
    
    highest_score = cursor.fetchone()
    return None if highest_score is None else highest_score[0]

def get_topic_id(test_id):
    cursor.execute(f"SELECT topic_id FROM tests WHERE test_id = {test_id}")
    
    topic_id = cursor.fetchone()[0]
    return topic_id

def add_highest_score(user_id, test_id, score):
    cursor.execute(f"""
                   INSERT INTO test_results(user_id, test_id, score)
                   VALUES({user_id}, {test_id}, {score});
                   """)
    
    conn.commit()

def edit_highest_score(user_id, test_id, score_dif):
    cursor.execute(f"""
                   UPDATE test_results
                   SET score = score + {score_dif}
                   WHERE user_id = {user_id} AND test_id = {test_id};
                   """)
    
    conn.commit()

def add_test_answers(user_id, test_answers):
    values = []
    for question in test_answers.questions:
        answer = question.answers[0]
        values.append(f"('{answer.content}', {answer.correctness}, '{datetime.now()}', {question.id}, {user_id})")
    
    cursor.execute(f"""
                   INSERT INTO test_answers(answer_content, correctness, date, question_id, user_id)
                   VALUES{', '.join(values)};
                   """)
    
    conn.commit()
    