import db.users, db.topics, db.tests, db.articles



def greet_user(user):
    msg = f'''Ваш профиль:
Имя: {user.first_name}
Фамилия: {user.last_name}
Группа: {user.student_group}

Ваш рейтинг: {user.rating}
'''
    return msg

def get_topic(topic_id):
    topic_name = db.topics.get_name(topic_id)
    article_names = db.articles.get_articles(topic_id)
    test_names = db.tests.get_tests(topic_id)
    
    article_msg = "\n".join([article['name'] for article in article_names])
    test_msg = "\n".join([test['name'] for test in test_names])
    
    
    msg = f'''Название топика:   {topic_name}

Статьи: 
{article_msg}

Тесты:
{test_msg}
'''

    return msg

def get_topics():
    topics = db.topics.get_all_topics()
    msg = 'Список топиков:\n\n'
    msg += '\n'.join([f"{idx+1}  →  {topic['name']}" for idx, topic in enumerate(topics)])
    return msg

def get_tests(topic_id):
    tests = db.tests.get_tests(topic_id)
    topic_name = db.topics.get_name(topic_id)
    msg = f'Список тестов для топика {topic_name}:\n\n'
    msg += '\n'.join([f"{idx+1}  →  {test['name']}" for idx, test in enumerate(tests)])
    return msg

def get_articles(topic_id):
    articles = db.articles.get_articles(topic_id)
    topic_name = db.topics.get_name(topic_id)
    msg = f'Список статей для топика {topic_name}:\n\n'
    msg += '\n'.join([f"{idx+1}  →  {article['name']}" for idx, article in enumerate(articles)])
    return msg
    


def admin_msg_handler(message):
    user_id = message.chat.id
    if message.text.startswith('В главное меню'):
        db.users.set_action(user_id, 'back_to_main')
    elif message.text.startswith('Топики'):
        db.users.set_action(user_id, 'edit_topic')