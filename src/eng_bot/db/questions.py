import psycopg2

from config import dbname, user, password, host

conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
cursor = conn.cursor()

def get_question_types():
    cursor.execute(f"SELECT type_id, name FROM question_types")
    
    question_types = [{"id": type_id, "name": name} for type_id, name in cursor.fetchall()]
    return question_types