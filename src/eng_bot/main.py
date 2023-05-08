import telebot

from config import bot_token
import db.users, db.topics, db.tests, db.articles, db.questions
import markups
import models
import msgs

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def start(message):
    db.users.create(message.chat.id)
    bot.send_message(message.chat.id, 'Добро пожаловать в @Mega_EngBot!', reply_markup=markups.get_reply_keyboard('greet'))
    bot.register_next_step_handler(message, greet_handler)

@bot.message_handler(commands=['admin'])
def admin(message):
    user_id = message.chat.id
    db.users.set_action(user_id, None)
    db.users.set_selection(user_id, None)
    
    if db.users.get_status(user_id) == 'admin':
        db.users.set_action(user_id, 'admin_main')
        admin_mode(message)
    else:
        bot.send_message(message.chat.id, 'У вас недостаточно прав!', reply_markup=markups.get_reply_keyboard('main', user_id))
        
@bot.message_handler(content_types=['text'])
def command_handler(message):
    user_id = message.chat.id
    db.users.create(user_id)
    if message.text.startswith('Регистрация'):
        if db.users.check_registration(user_id):
            bot.send_message(message.chat.id, 'Вы уже зарегистрированы!', reply_markup=markups.get_reply_keyboard('main', user_id))
        else:
            reg_handler(message)
    elif message.text.startswith('Профиль'):
        if not db.users.check_registration(user_id):
            bot.send_message(message.chat.id, 'Вы еще не зарегистрированы!', reply_markup=markups.get_reply_keyboard('main', user_id))
        else:
            profile(message)
    elif message.text.startswith('Топики'):
        view_topics(message)
    elif message.text.startswith('Таблица лидеров'):
        pass

def view_topics(message):
    user_id = message.chat.id
    db.users.set_selection(user_id, None)
    
    msg = msgs.get_topics()
    
    bot.send_message(message.chat.id, msg, reply_markup=markups.get_inline_keyboard('student_topic_list'))


@bot.callback_query_handler(func=lambda call: call.data.startswith('student_topics_'))
def student_topics_callback_worker(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    
    topic_id = call.data.split('_')[2]
    
    try:
        db.users.set_selection(user_id, topic_id)
        msg = msgs.get_topic(topic_id)
    except:
        msg = 'Произошла ошибка'

    bot.edit_message_text(chat_id=user_id, message_id=message_id, text=msg, reply_markup=markups.get_inline_keyboard('student_topic_next_step'))

@bot.callback_query_handler(func=lambda call: call.data.startswith('student_topic_'))
def student_topic_callback_worker(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    
    answer = '_'.join(call.data.split('_')[2:])
    if answer == 'back':
        db.users.set_selection(user_id, None)
        msg = msgs.get_topics()
        
        bot.edit_message_text(chat_id=user_id, message_id=message_id, text=msg, reply_markup=markups.get_inline_keyboard('student_topic_list'))
    elif answer == 'view_tests':
        topic_id = db.users.get_selection(user_id)
        msg = msgs.get_tests(topic_id)
        
        bot.edit_message_text(chat_id=user_id, message_id=message_id, text=msg, reply_markup=markups.get_inline_keyboard('student_view_tests', data=topic_id))
        
    elif answer == 'view_articles':
        topic_id = db.users.get_selection(user_id)
        msg = msgs.get_articles(topic_id)
        
        bot.edit_message_text(chat_id=user_id, message_id=message_id, text=msg, reply_markup=markups.get_inline_keyboard('student_view_articles', data=topic_id))
    

@bot.callback_query_handler(func=lambda call: call.data.startswith('student_tests_'))
def student_tests_callback_worker(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    
    test_id = '_'.join(call.data.split('_')[2:])
    if test_id == 'back':
        msg = msgs.get_topics()
        bot.edit_message_text(chat_id=user_id, message_id=message_id, text=msg, reply_markup=markups.get_inline_keyboard('student_topic_list'))
    else:
        db.users.set_selection(user_id, test_id)
    

@bot.callback_query_handler(func=lambda call: call.data.startswith('student_acrticles_'))
def student_articles_callback_worker(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    
    article_id = '_'.join(call.data.split('_')[2:])
    if article_id == 'back':
        msg = msgs.get_topics()
        bot.edit_message_text(chat_id=user_id, message_id=message_id, text=msg, reply_markup=markups.get_inline_keyboard('student_topic_list'))
    else:
        db.users.set_selection(user_id, article_id)


# =====================================ADMIN=====================================
def admin_mode(message):
    user_id = message.chat.id
    action = db.users.get_action(user_id)
    if action == 'admin_main':
        bot.send_message(message.chat.id, 'Вы в админ-меню.', reply_markup=markups.get_reply_keyboard('admin_main', one_time=True))
        bot.register_next_step_handler(message, msgs.admin_msg_handler)
        bot.register_next_step_handler(message, admin_mode)
    elif action == 'back_to_main':
        db.users.set_action(user_id, None)
        bot.send_message(message.chat.id, 'Добро пожаловать в главное меню!', reply_markup=markups.get_reply_keyboard('main', user_id))
    elif action == 'edit_topic':
        edit_topic(message)


def edit_topic(message):
    user_id = message.chat.id
    db.users.set_selection(user_id, None)
    
    msg = msgs.get_topics()
    
    bot.send_message(message.chat.id, msg, reply_markup=markups.get_inline_keyboard('admin_topic_list'))


def add_test_handler(message):
    def add_test(message):
        def add_question(message):
            def add_answer(message):
                action = db.users.get_action(user_id)
                
                if action == 'add_answer_content':
                    db.users.set_action(user_id, 'add_answer_correctness')
                    answer.content = message.text
                    
                    bot.send_message(message.chat.id, 'Добавьте правильность ответа', reply_markup=markups.get_reply_keyboard('true_false', one_time=True))
                    bot.register_next_step_handler(message, add_answer)
                elif action == 'add_answer_correctness':
                    db.users.set_action(user_id, 'answer_next_step')
                    answer.correctness = True if message.text.startswith('Верно') else False
                    
                    bot.send_message(message.chat.id, 'Выберете следующее действие', reply_markup=markups.get_reply_keyboard('answer_next_step', one_time=True))
                    bot.register_next_step_handler(message, add_answer)
                elif action == 'answer_next_step':
                    if message.text.startswith('Вернуться'):
                        question.add_answer(answer)
                        test.add_question(question)
                        
                        db.tests.add(user_id, topic_id, test)
                        edit_topic(message)
                    elif message.text.startswith('Добавить тест'):
                        question.add_answer(answer)
                        test.add_question(question)
                        
                        db.tests.add(user_id, topic_id, test)
                        add_test_handler(message)
                    elif message.text.startswith('Добавить вопрос'):
                        question.add_answer(answer)
                        test.add_question(question)
                        
                        db.users.set_action(user_id, 'add_question_content')
                        add_test(message)
                    elif message.text.startswith('Добавить ответ'):
                        question.add_answer(answer)
                        
                        db.users.set_action(user_id, 'add_answer_content')
                        add_question(message)
            
            question_types = db.questions.get_question_types()
            action = db.users.get_action(user_id)
            if action == 'add_question_content':
                db.users.set_action(user_id, 'add_question_type')
                question.content = message.text
                
                bot.send_message(message.chat.id, 'Выберете тип вопроса', reply_markup=markups.get_reply_keyboard("question_types", data=question_types, one_time=True))
                bot.register_next_step_handler(message, add_question)
            elif action == 'add_question_type':
                db.users.set_action(user_id, 'add_question_price')
                question.type = list(filter(lambda x: x["name"] == message.text, question_types))[0]["id"]
                
                bot.send_message(message.chat.id, 'Введите цену вопроса (для таблицы лидеров)')
                bot.register_next_step_handler(message, add_question)
            elif action == 'add_question_price':
                db.users.set_action(user_id, 'add_answer_content')
                question.price = message.text
                answer = models.Answer()
                
                bot.send_message(message.chat.id, 'Добавьте вариант ответа')
                bot.register_next_step_handler(message, add_answer)
            elif action == 'add_answer_content':
                answer = models.Answer()
                
                bot.send_message(message.chat.id, 'Добавьте вариант ответа')
                bot.register_next_step_handler(message, add_answer)
                
        action = db.users.get_action(user_id)
        if action == 'add_test':
            db.users.set_action(user_id, 'add_test_name')
            bot.send_message(message.chat.id, 'Введите название теста')
            bot.register_next_step_handler(message, add_test)
        elif action == 'add_test_name':
            db.users.set_action(user_id, 'add_question_content')
            test.name = message.text
            question = models.Question()
            
            bot.send_message(message.chat.id, 'Введите формулировку вопроса')
            bot.register_next_step_handler(message, add_question)
        elif action == 'add_question_content':
            question = models.Question()
            
            bot.send_message(message.chat.id, 'Введите формулировку вопроса')
            bot.register_next_step_handler(message, add_question)
    
    test = models.Test()
    user_id = message.chat.id
    topic_id = db.users.get_selection(user_id)
    db.users.set_action(user_id, 'add_test')
    add_test(message)


def add_article_handler(message):
    def add_article(message):
        action = db.users.get_action(user_id)
        
        if action == 'add_article':
            db.users.set_action(user_id, 'add_article_name')
            
            bot.send_message(message.chat.id, 'Введите название статьи')
            bot.register_next_step_handler(message, add_article)
        elif action == 'add_article_name':
            db.users.set_action(user_id, 'add_article_link')
            article.name = message.text
            
            bot.send_message(message.chat.id, 'Введите ссылку на статью')
            bot.register_next_step_handler(message, add_article)
        elif action == 'add_article_link':
            db.users.set_action(user_id, 'article_next_step')
            article.link = message.text
            db.articles.add_article(user_id, topic_id, article)
            
            bot.send_message(message.chat.id, 'Выберете следующее действие', reply_markup=markups.get_reply_keyboard('article_next_step', one_time=True))
            bot.register_next_step_handler(message, add_article)
        elif action == 'article_next_step':
            if message.text.startswith('Вернуться'):
                edit_topic(message)
            elif message.text.startswith('Добавить статью'):
                add_article_handler(message)
            
    article = models.Article()
    
    user_id = message.chat.id
    topic_id = db.users.get_selection(user_id)
    db.users.set_action(user_id, 'add_article')
    add_article(message)


def profile(message):
    DATA = db.users.get_user(message.chat.id)
    user = models.User(DATA)
    msg = msgs.greet_user(user)
    
    bot.send_message(message.chat.id, msg)


def greet_handler(message):
    user_id = message.chat.id
    if message.text.startswith('Что я такое'):
        bot.send_message(message.chat.id, 'Я вот могу...', reply_markup=markups.get_reply_keyboard('getit'))
        bot.register_next_step_handler(message, greet_handler)
    else:
        bot.send_message(message.chat.id, 'Добро пожаловать в главное меню!', reply_markup=markups.get_reply_keyboard('main', user_id))


def reg_handler(message):
    user_id = message.chat.id
    
    if db.users.get_first_name(user_id) and db.users.get_last_name(user_id) and db.users.get_group(user_id):
        db.users.set_action(user_id, 'NULL')
        db.users.set_registration(user_id, True)
        bot.send_message(message.chat.id, 'Спасибо за регистрацию!', reply_markup=markups.get_reply_keyboard('main', user_id))
    
    if db.users.get_first_name(user_id) is None:
        if db.users.get_action(user_id) == 'set_first_name':
            db.users.set_first_name(user_id, message.text)
            reg_handler(message)
        else:
            bot.send_message(message.chat.id, 'Введите свое имя', reply_markup=markups.delete_markup())
            db.users.set_action(user_id, 'set_first_name')
            bot.register_next_step_handler(message, reg_handler)
    
    elif db.users.get_last_name(user_id) is None:
        if db.users.get_action(user_id) == 'set_last_name':
            db.users.set_last_name(user_id, message.text)
            reg_handler(message)
        else:
            bot.send_message(message.chat.id, 'Введите свою фамилию', reply_markup=markups.delete_markup())
            db.users.set_action(user_id, 'set_last_name')
            bot.register_next_step_handler(message, reg_handler)
    
    elif db.users.get_group(user_id) is None:
        if db.users.get_action(user_id) == 'set_group':
            db.users.set_group(user_id, message.text)
            reg_handler(message)
        else:
            bot.send_message(message.chat.id, 'Введите свою группу', reply_markup=markups.delete_markup())
            db.users.set_action(user_id, 'set_group')
            bot.register_next_step_handler(message, reg_handler)
        

@bot.callback_query_handler(func=lambda call: call.data.startswith('admin_topics_'))
def admin_topics_callback_worker(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    
    topic_id = call.data.split('_')[2]

    if topic_id == 'back':
        db.users.set_action(user_id, 'admin_main')
        admin_mode(call.message)
        return
    else:
        db.users.set_selection(user_id, topic_id)
        try:
            msg = msgs.get_topic(topic_id)
        except:
            msg = 'Произошла ошибка'

    bot.edit_message_text(chat_id=user_id, message_id=message_id, text=msg, reply_markup=markups.get_inline_keyboard('admin_topic_next_step'))

@bot.callback_query_handler(func=lambda call: call.data.startswith('admin_topic_'))
def admin_topic_callback_worker(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    
    answer = '_'.join(call.data.split('_')[2:])
    if answer == 'back':
        db.users.set_selection(user_id, None)
        msg = msgs.get_topics()
        
        bot.edit_message_text(chat_id=user_id, message_id=message_id, text=msg, reply_markup=markups.get_inline_keyboard('admin_topic_list'))
    elif answer == 'edit_tests':
        bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id, reply_markup=markups.get_inline_keyboard('admin_edit_test'))
    elif answer == 'edit_articles':
        bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id, reply_markup=markups.get_inline_keyboard('admin_edit_article'))

@bot.callback_query_handler(func=lambda call: call.data.startswith('admin_test_'))
def admin_test_callback_worker(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    
    answer = '_'.join(call.data.split('_')[2:])
    if answer == 'back':
        call.data = f'topics_{db.users.get_selection(user_id)}'
        admin_topics_callback_worker(call)
        return
    elif answer == 'add':
        add_test_handler(call.message)
    elif answer == 'edit':
        pass
    elif answer == 'delete':
        pass

@bot.callback_query_handler(func=lambda call: call.data.startswith('admin_article_'))
def admin_article_callback_worker(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    
    answer = '_'.join(call.data.split('_')[2:])
    if answer == 'back':
        call.data = f'topics_{db.users.get_selection(user_id)}'
        admin_topics_callback_worker(call)
        return
    elif answer == 'add':
        add_article_handler(call.message)
    elif answer == 'edit':
        pass
    elif answer == 'delete':
        pass

bot.infinity_polling(timeout=10, long_polling_timeout=5)