import db.users, db.topics, db.tests, db.articles, db.questions



def greet_user(user):
    msg = f'''Ваш профиль:
Имя: {user.first_name}
Фамилия: {user.last_name}
Группа: {user.student_group}

Ваш рейтинг: {user.score}
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
        
def get_test_stats(user_id, test_id):
    test = db.tests.get_test(test_id)
    test_by = db.users.get_user(test["user_id"])
    
    highest_score = db.tests.get_highest_score(user_id, test_id)
    questions = db.questions.get_questions(test_id)
    questions_amount = len(questions)
    questions_price = sum([question["price"] for question in questions])
    
    msg = f"{test['name']}:\n"
    msg += "Создатель теста: Аноним\n\n" if test_by["last_name"] is None or test_by["first_name"] is None \
                                else f"Создатель теста: {test_by['last_name']} {test_by['first_name']}\n\n"
    msg += f"Количество вопросов: {questions_amount}\n"

    msg += "Вы ранее не проходили этот тест!" if highest_score is None else f"Ваш лучший результат: {highest_score}/{questions_price}"
    return msg

def get_test_ending(test_name, correct_answers, total_answers, score_dif):
    msg = f"Ваш результат: {correct_answers}/{total_answers}.\n"
    
    if correct_answers == total_answers:
        msg += "Поздравляю, Вы набрали максимальный балл!\n"
        if score_dif <= 0:
            return msg
    
    if score_dif > 0:
        msg += f"Вы получили {score_dif} {year_type(score_dif)}.\n"
    else:
        msg += "Вы набрали недостаточно баллов для награды 😢\n"
    
    return msg

def year_type(age):
    if age % 10 in [2, 3, 4]:
        return 'балла'
    elif age % 10 != 1 or age % 100 == 11:
        return 'баллов'
    else:
        return 'балл'
 