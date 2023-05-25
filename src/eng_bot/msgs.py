import db.users, db.topics, db.tests, db.articles, db.questions

about_msg = '''
🌟 @Mega_EngBot — ваш лучший Telegram-бот для изучения английского языка! 📚🌍

🧠 Проходите увлекательне тесты
📖 Читайте занимательные статьи
🏆 Соревнуйтесь в таблицe лидеров

🚀 Отправляйтесь в это захватывающее приключение по изучению английского языка вместе с нами уже сегодня! 🎉✨
'''

numbers = {'0':'0️⃣','1':'1️⃣','2':'2️⃣','3':'3️⃣','4':'4️⃣','5':'5️⃣','6':'6️⃣','7':'7️⃣','8':'8️⃣','9':'9️⃣'}
medals = {'1':'🥇','2':'🥈','3':'🥉'}

def greet_user(user):
    msg = f'''
📷 Ваш профиль:

🙋‍♂️ Имя:             {user.first_name}
📛 Фамилия:   {user.last_name}
🎓 Группа:       {user.student_group}
⭐️ Рейтинг:     {user.score}
'''
    return msg

def get_topic(topic_id):
    topic_name = db.topics.get_name(topic_id)
    msg = f'📇 Название топика:  {topic_name}\n\n'
    
    article_names = db.articles.get_articles(topic_id)
    test_names = db.tests.get_tests(topic_id)
    
    if article_names:
        article_msg = "\n".join([f'►  {article["name"]}' for article in article_names])
        msg += f'📖 Статьи:\n{article_msg}\n\n'
    
    if test_names:
        test_msg = "\n".join([f'►  {test["name"]}' for test in test_names])
        msg += f'🧠 Тесты:\n{test_msg}\n'
    
    if not article_names and not test_names:
        msg += 'В этот топик еще не успели что-то добавить 😔'
    
    return msg

def get_topics():
    topics = db.topics.get_all_topics()
    msg = '🗂️ Список топиков:\n\n'
    msg += '\n'.join([f"{get_number(idx+1)}  →  {topic['name']}" for idx, topic in enumerate(topics)])
    return msg

def get_leader_board(user_id):
    leader_board = db.users.get_leader_board_data()
    
    msg = '🏆 Таблица лидеров:\n\n'
    
    for idx, user in enumerate(leader_board):
        user_name = user['first_name'] if user['is_registered'] else str(user['user_id'])[:3]+('*'*5)
        msg += f'{get_number(idx+1) if idx > 2 else medals[str(idx+1)]} ► {user_name} ◄ {user["score"]} очк.\n'
    
    return msg

def get_number(value):
    text = str(value)
    for num, emoji in numbers.items():
        text = text.replace(num, emoji)
    return text

def get_tests(topic_id):
    tests = db.tests.get_tests(topic_id)
    topic_name = db.topics.get_name(topic_id)
    msg = f'📄 Список тестов для топика {topic_name}:\n\n'
    msg += '\n'.join([f"►  {test['name']}" for test in tests])
    return msg

def get_articles(topic_id):
    articles = db.articles.get_articles(topic_id)
    topic_name = db.topics.get_name(topic_id)
    msg = f'📄 Список статей для топика {topic_name}:\n\n'
    msg += '\n'.join([f"►  {article['name']}" for article in articles])
    return msg

def admin_msg_handler(message):
    user_id = message.chat.id
    if message.text.startswith('В главное меню'):
        db.users.set_action(user_id, 'back_to_main')
    elif message.text.startswith('Топики'):
        db.users.set_action(user_id, 'edit_topic')
    elif message.text.startswith('Создать топик'):
        db.users.set_action(user_id, 'add_topic')
    elif message.text.startswith('Удалить топик'):
        db.users.set_action(user_id, 'del_topic')
        
def get_test_info(user_id, test_id):
    test = db.tests.get_test(test_id)
    test_by = db.users.get_user(test["user_id"])
    
    highest_score = db.tests.get_highest_score(user_id, test_id)
    questions = db.questions.get_questions(test_id)
    questions_amount = len(questions)
    questions_price = sum([question["price"] for question in questions])
    
    msg = f"📋 Тест: {test['name']}\n\n"
    msg += "👨‍💻 Создатель теста: Аноним\n" if test_by["last_name"] is None or test_by["first_name"] is None \
                                else f"👨‍💻 Создатель теста: {test_by['last_name']} {test_by['first_name']}\n"
    msg += f"🔢 Количество вопросов: {questions_amount}\n"

    msg += "❗ Вы ранее не проходили этот тест" if highest_score is None else f"🌟 Ваш лучший результат: {highest_score}/{questions_price}"
    return msg

def get_test_results(answers):
    msg = '📝 Ваши ответы:\n\n'
    for idx, answer in enumerate(answers):
        q_content = db.questions.get_content(answer['question_id'])
        msg += f'{idx+1}. {q_content}\n     ►  {answer["answer_content"]}  '
        if answer["correctness"]:
            msg += '✅\n'
        else:
            msg += '❌\n'
        
    return msg
        
def get_article_info(article_id):
    article = db.articles.get_article(article_id)
    article_by = db.users.get_user(article["user_id"])
    
    msg = f"📋 Статья: {article['name']}\n"
    msg += "👨‍💻 Создатель теста: Аноним\n\n" if article_by["last_name"] is None or article_by["first_name"] is None \
                                else f"👨‍💻 Создатель теста: {article_by['last_name']} {article_by['first_name']}\n\n"
    
    msg += f"ℹ️ Описание: {article['description']}" if article['description'] else "ℹ️ Описание к данной статье отсутствует."
    return msg
    
def get_test_ending(correct_answers, total_answers, score_dif):
    msg = f"🎯 Ваш результат: {correct_answers}/{total_answers}.\n\n"
    
    if correct_answers == total_answers:
        msg += "👏 Поздравляю, вы набрали максимальный балл!\n"
        if score_dif <= 0:
            return msg
    
    if score_dif > 0:
        msg += f"👏 Вы получили {score_dif} {score_type(score_dif)}.\n"
    else:
        msg += "Вы набрали недостаточно баллов для награды 😢\n"
    
    return msg

def score_type(score):
    if score % 10 in [2, 3, 4]:
        return 'балла'
    elif score % 10 != 1 or score % 100 == 11:
        return 'баллов'
    else:
        return 'балл'
 