import psycopg2

from config import dbname, user, password, host

conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
cursor = conn.cursor()

def get_tests(topic_id):
    cursor.execute(f"SELECT name, test_id, user_id FROM tests WHERE topic_id = {topic_id}")
    tests = cursor.fetchall()
    result = [{'name': test[0], 'id': test[1], 'user_id': test[2]} for test in tests]
    return result

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