from telebot import types
import db.users, db.topics, db.tests, db.articles, db.questions

def get_reply_keyboard(type, data=None, one_time=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time)
    
    profile = types.KeyboardButton('Профиль')
    topics = types.KeyboardButton('Топики')
    leader_board = types.KeyboardButton('Таблица лидеров')
    
    articles = types.KeyboardButton('Статьи')
    tests = types.KeyboardButton('Тесты')
    
    register = types.KeyboardButton('Регистрация')
    
    what = types.KeyboardButton('Что я такое?')
    skip = types.KeyboardButton('Пропустить')
    
    getit = types.KeyboardButton('Понятно!')
    
    topics = types.KeyboardButton('Топики')
    back_to_main = types.KeyboardButton('В главное меню')
    
    edit_test = types.KeyboardButton('Редактировать тесты')
    edit_article = types.KeyboardButton('Редактировать статьи')
    
    back = types.KeyboardButton('Вернуться')
    
    it_is_true = types.KeyboardButton('Верно')
    it_is_false = types.KeyboardButton('Не верно')
    
    new_test = types.KeyboardButton('Добавить тест')
    new_question = types.KeyboardButton('Добавить вопрос')
    new_answer = types.KeyboardButton('Добавить ответ')
    
    new_article = types.KeyboardButton('Добавить статью')
    
    back_to_admin = types.KeyboardButton('К топикам')
    
    if type == 'main':
        if db.users.check_registration(data):
            markup.add(profile)
        else:
            markup.add(register)
        markup.add(topics, leader_board)
    elif type == 'greet':
        markup.add(what, skip)
    elif type == 'getit':
        markup.add(getit)
    elif type == 'admin_main':
        markup.add(topics)
        markup.add(back_to_main)
    elif type == 'admin_edit_test_art':
        markup.add(edit_test, edit_article)
        markup.add(back)
    elif type == 'true_false':
        markup.add(it_is_true, it_is_false)
    elif type == 'answer_next_step':
        markup.add(new_answer, new_question)
        markup.add(new_test)
        markup.add(back)
    elif type == 'article_next_step':
        markup.add(new_article, back)
    elif type == 'question_types':
        question_types = db.questions.get_question_types()
        temp_list = []
        for idx, type in enumerate(question_types):
            item = types.KeyboardButton(type["name"])
            temp_list.append(item)
            if (idx + 1) % 3 == 0:
                markup.add(*temp_list)
                temp_list = []
        
        markup.add(*temp_list)
        
    
    return markup

def get_inline_keyboard(type, data=None):
    markup = types.InlineKeyboardMarkup()
    
    if type == 'admin_topic_list':
        temp_list = []
        data = db.topics.get_all_topics()
        for idx, topic in enumerate(data):
            if len(topic['name']) > 14:
                topic_name = f'{topic["name"].strip()[:14]}...'
            else:
                topic_name = topic["name"]
            item = types.InlineKeyboardButton(text=topic_name, callback_data=f'admin_topics_{topic["id"]}')
            temp_list.append(item)
            if (idx + 1) % 3 == 0:
                markup.add(*temp_list)
                temp_list = []
        
        markup.add(*temp_list)
        
        topics_back = types.InlineKeyboardButton(text='Вернуться', callback_data='admin_topics_back')
        markup.add(topics_back)
        
    elif type == 'admin_topic_next_step':
        topic_back = types.InlineKeyboardButton(text='Вернуться', callback_data='admin_topic_back')
        topic_edit_tests = types.InlineKeyboardButton(text='Изменить тесты', callback_data='admin_topic_edit_tests')
        topic_edit_articles = types.InlineKeyboardButton(text='Изменить статьи', callback_data='admin_topic_edit_articles')
        
        markup.add(topic_edit_tests, topic_edit_articles)
        markup.add(topic_back)
    
    elif type == 'admin_edit_test':
        test_add = types.InlineKeyboardButton(text='Добавить тест', callback_data='admin_test_add')
        test_edit = types.InlineKeyboardButton(text='Редактировать тест', callback_data='admin_test_edit')
        test_delete = types.InlineKeyboardButton(text='Удалить тест', callback_data='admin_test_delete')
        test_back = types.InlineKeyboardButton(text='Вернуться', callback_data='admin_test_back')
        
        markup.add(test_add)
        markup.add(test_edit, test_delete)
        markup.add(test_back)
    
    elif type == 'admin_edit_article':
        art_add = types.InlineKeyboardButton(text='Добавить статью', callback_data='admin_article_add')
        art_edit = types.InlineKeyboardButton(text='Редактировать статью', callback_data='admin_article_edit')
        art_delete = types.InlineKeyboardButton(text='Удалить статью', callback_data='admin_article_delete')
        art_back = types.InlineKeyboardButton(text='Вернуться', callback_data='admin_article_back')
        
        markup.add(art_add)
        markup.add(art_edit, art_delete)
        markup.add(art_back)
    
    elif type == 'student_topic_list':
        temp_list = []
        topics = db.topics.get_all_topics()
        for idx, topic in enumerate(topics):
            if len(topic['name'].strip()) > 14:
                topic_name = f'{topic["name"].strip()[:14]}...'
            else:
                topic_name = topic["name"]
            item = types.InlineKeyboardButton(text=topic_name, callback_data=f'student_topics_{topic["id"]}')
            temp_list.append(item)
            if (idx + 1) % 3 == 0:
                markup.add(*temp_list)
                temp_list = []
        
        markup.add(*temp_list)
    
    elif type == 'student_topic_next_step':
        topic_back = types.InlineKeyboardButton(text='Вернуться', callback_data='student_topic_back')
        topic_edit_tests = types.InlineKeyboardButton(text='Пройти тест', callback_data='student_topic_view_tests')
        topic_edit_articles = types.InlineKeyboardButton(text='Посмотреть статью', callback_data='student_topic_view_articles')
        
        markup.add(topic_edit_tests, topic_edit_articles)
        markup.add(topic_back)
    
    elif type == 'student_view_tests':
        temp_list = []
        topic_id = data
        tests = db.tests.get_tests(topic_id)
        for idx, test in enumerate(tests):
            if len(test['name'].strip()) > 14:
                test_name = f'{test["name"].strip()[:14]}...'
            else:
                test_name = test["name"]
            item = types.InlineKeyboardButton(text=test_name, callback_data=f'student_tests_{test["id"]}')
            temp_list.append(item)
            if (idx + 1) % 3 == 0:
                markup.add(*temp_list)
                temp_list = []
        markup.add(*temp_list)
        
        student_tests_back = types.InlineKeyboardButton(text='Вернуться', callback_data=f'student_topics_{topic_id}')
        markup.add(student_tests_back)
    
    elif type == 'student_view_articles':
        temp_list = []
        topic_id = data
        acrticles = db.articles.get_articles(topic_id)
        for idx, acrticle in enumerate(acrticles):
            if len(acrticle['name'].strip()) > 14:
                acrticle_name = f'{acrticle["name"].strip()[:14]}...'
            else:
                acrticle_name = acrticle["name"]
            item = types.InlineKeyboardButton(text=acrticle_name, callback_data=f'student_acrticles_{acrticle["id"]}')
            temp_list.append(item)
            if (idx + 1) % 3 == 0:
                markup.add(*temp_list)
                temp_list = []
        markup.add(*temp_list)
        
        student_articles_back = types.InlineKeyboardButton(text='Вернуться', callback_data=f'student_topics_{topic_id}')
        markup.add(student_articles_back)
    
    elif type == 'start_test':
        test_start = types.InlineKeyboardButton(text='Начать тестирование!', callback_data=f'start_test_{data}')
        test_back = types.InlineKeyboardButton(text='Вернуться', callback_data='student_topic_view_tests')
        markup.add(test_start, test_back)

    return markup
        
        

def delete_markup():
    markup = types.ReplyKeyboardRemove()
    return markup