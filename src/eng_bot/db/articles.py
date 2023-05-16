import psycopg2

from config import dbname, user, password, host

conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
cursor = conn.cursor()

def get_articles(topic_id):
    cursor.execute(f"SELECT name, article_id, user_id FROM articles WHERE topic_id = {topic_id}")
    articles = cursor.fetchall()
    result = [{'name': article[0], 'id': article[1], 'user_id': article[2]} for article in articles]
    return result

def get_article(article_id):
    cursor.execute(f"SELECT link, name, topic_id, user_id, description FROM articles WHERE article_id = {article_id}")
    temp = cursor.fetchone()
    article = {"link": temp[0], "name": temp[1], "topic_id": temp[2], "user_id": temp[3], "description": temp[4]}
    return article
    

def add_article(user_id, topic_id, article):
    cursor.execute(f"""
                   INSERT INTO articles(link, name, topic_id, user_id) 
                   VALUES('{article.link}', '{article.name}', {topic_id}, {user_id})
                   """)
    conn.commit()