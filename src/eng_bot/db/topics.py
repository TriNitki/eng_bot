import psycopg2

from config import dbname, user, password, host

import db.users

conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
cursor = conn.cursor()


def create(topic_name, user_id):
    cursor.execute(f"INSERT INTO topics(name, user_id) VALUES('{topic_name}', {user_id})")
    conn.commit()
    
    topic_id = get_id(topic_name, user_id)
    db.users.set_selection(user_id, topic_id)

def get_name(topic_id):
    cursor.execute(f"SELECT name FROM topics WHERE topic_id = {topic_id}")
    topic_name = cursor.fetchone()[0]
    return topic_name

def get_all_topics():
    cursor.execute(f"SELECT name, topic_id, user_id FROM topics")
    topics = cursor.fetchall()
    result = [{'name': topic[0], 'id': topic[1], 'user_id': topic[2]} for topic in topics]
    return result

def get_id(topic_name, user_id=None):
    if user_id:
        cursor.execute(f"SELECT topic_id FROM topics WHERE name = '{topic_name}' AND user_id = {user_id}")
    else:
        cursor.execute(f"SELECT topic_id FROM topics WHERE name = '{topic_name}'")
    topic_id = cursor.fetchone()[0]
    return topic_id