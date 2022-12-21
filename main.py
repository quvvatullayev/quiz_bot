from telegram.ext import Updater,MessageHandler,Filters,CallbackContext,CommandHandler,CallbackQueryHandler,StringCommandHandler
from telegram import Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
import requests
import json
import pprint
TOKEN = '5677023630:AAGdskZAvZwdRix213Ho28QaN-NZVcQtuU8'
b_url = 'http://127.0.0.1:8000'
class Quiz_bot:
    true = 0
    false = 0
    """xato bajardim vaqtinchalik question_list_index ni argumint deb"""
    question_list_index = []

    def start(self, update:Update, context:CallbackContext):
        id = update.message.from_user.id
        updater.bot.sendMessage(id, 'Hush kelibsiz')
        url = f"{b_url}/api/student/"

        first_name = update.message.from_user.first_name
        if first_name == None:
            first_name = None
        last_name = update.message.from_user.last_name
        if last_name == None:
            last_name = None
        telegram_id = update.message.chat.id
        if telegram_id == None:
            telegram_id = None
        username = update.message.from_user.username
        if username == None:
            username = None
        json_data = {'first_name': first_name, 'last_name': last_name, 'telegram_id': telegram_id, 'username': username}
        
        r_post = requests.post(url=url, json=json_data)

    def quiz(self, update:Update, context:CallbackContext):
        id = update.message.from_user.id
        url = f'{b_url}/api/quiz/'
        rq = requests.get(url)
        data_json = rq.json()

    
        inline_key = []
        for i in data_json:
            ed = i['id']
            inline_key.append([InlineKeyboardButton(i['title'], callback_data=f'🥇{ed}')])
        reply_markup = InlineKeyboardMarkup(inline_key)
        updater.bot.sendMessage(id, 'Fanlar ro\'yxati', reply_markup=reply_markup)
    
    def quer_start(self, update:Update, context:CallbackContext):
        quer = update.callback_query
        url = f'{b_url}/api/quiz/'
        rq = requests.get(url)
        data_json = rq.json()

        inline_key = []
        for i in data_json:
            ed = i['id']
            inline_key.append([InlineKeyboardButton(i['title'], callback_data=f'🥇{ed}')])
        reply_markup = InlineKeyboardMarkup(inline_key)
        quer.edit_message_text("Fanlar ro\'yxati", reply_markup=None)
        quer.edit_message_reply_markup(reply_markup=reply_markup)

    def topic(self, update:Update, context:CallbackContext):
        quer = update.callback_query
        pk = quer.data[1:]
        url = f'{b_url}/api/topic/{pk}/'
        rq = requests.get(url)
        data_json = rq.json() 

        inline_key = []
        for i in data_json['quiz']["topics"]:
            ed = i['id']
            inline_key.append([InlineKeyboardButton(i['title'], callback_data=f'📌🥈 {ed}')])
        inline_key.append([InlineKeyboardButton('⬅️ortga', callback_data='⬅️ortga')])
        reply_markup = InlineKeyboardMarkup(inline_key)
        quer.edit_message_text("Mavzular ro'yxati:", reply_markup=None)
        quer.edit_message_reply_markup(reply_markup=reply_markup)

    def border(self, update:Update, context:CallbackContext):
        quer = update.callback_query
        data =quer.data.split()
        topic_id = data[1]
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('5 ta', callback_data=f'🥈 {topic_id} {5}'), InlineKeyboardButton('10 ta', callback_data=f'🥈 {topic_id} {10}')],
            [InlineKeyboardButton('15 ta', callback_data=f'🥈 {topic_id} {15}'), InlineKeyboardButton('20 ta', callback_data=f'🥈 {topic_id} {20}')],
            [InlineKeyboardButton('25 ta', callback_data=f'🥈 {topic_id} {25}'), InlineKeyboardButton('30 ta', callback_data=f'🥈 {topic_id} {30}')],
            [InlineKeyboardButton('40 ta', callback_data=f'🥈 {topic_id} {40}'), InlineKeyboardButton('50 ta', callback_data=f'🥈 {topic_id} {50}')]
            ])
        quer.edit_message_text("Nechta test yechmoqchisiz:", reply_markup=reply_markup)

    def quitoin(self, update:Update, context:CallbackContext):
        quer = update.callback_query
        quer.edit_message_text("📌Savvollar:", reply_markup=None)
        data = quer.data.split()
        pk = data[1]
        n = int(data[2])
        url1 = f'{b_url}/api/question/{pk}/'
        rq = requests.get(url1)
        data_quitoin = rq.json()

        url_student = f"{b_url}/api/student/{quer.message.chat.id}/"
        r_user = requests.get(url_student)
        user_id = r_user.json()['id']

        url_result = f"{b_url}/api/result/"
        r = requests.post(url_result, json={"student":user_id, "topic":pk, "score":0})
        r_id = r.json()['id']

        list_data = data_quitoin['quiz']['topic']["questions_index"][:n]
        self.question_list_index = list_data

        if len(self.question_list_index) > 0:
            img = data_quitoin['quiz']['topic']['questions'][self.question_list_index[0]]["img"]
            
            inline_key = []
            for optons in data_quitoin['quiz']['topic']['questions'][self.question_list_index[0]]["options"]:
                    q_id = optons["question"]
                    o_id = optons['id']
                    inline_key.append([InlineKeyboardButton(optons["title"], callback_data=f"❔ {q_id} {o_id} {r_id} {pk}")])
                    
            reply_markup = InlineKeyboardMarkup(inline_key)
            text = data_quitoin['quiz']['topic']['questions'][self.question_list_index[0]]["title"]
            updater.bot.sendPhoto(quer.message.chat.id ,img, text, reply_markup = reply_markup)

            if len(self.question_list_index) > 0:
                self.question_list_index.pop(0)
        else:
            updater.bot.sendMessage(quer.message.chat.id, 'Bu mavzu bo\'yicha savollarimiz tugadi.')
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('✅testni tugatish', callback_data=f'✅ {pk} {user_id}'), InlineKeyboardButton('⬅️ortga', callback_data='⬅️ortga')]])
            updater.bot.sendMessage(quer.message.chat.id,'Yo\'nalishni tanlang',reply_markup=reply_markup)

    def quiston1(self, update:Update, context:CallbackContext, pk, r_id, id):
        url1 = f'{b_url}/api/question/{pk}/'
        rq = requests.get(url1)
        data_quitoin = rq.json()

        url_student = f"{b_url}/api/student/{id}/"
        r_user = requests.get(url_student)
        user_id = r_user.json()['id']

        if len(self.question_list_index) > 0:
            img = data_quitoin['quiz']['topic']['questions'][self.question_list_index[0]]["img"]
            
            inline_key = []
            for optons in data_quitoin['quiz']['topic']['questions'][self.question_list_index[0]]["options"]:
                    q_id = optons["question"]
                    o_id = optons['id']
                    inline_key.append([InlineKeyboardButton(optons["title"], callback_data=f"❔ {q_id} {o_id} {r_id} {pk}")])
                    
            reply_markup = InlineKeyboardMarkup(inline_key)
            text = data_quitoin['quiz']['topic']['questions'][self.question_list_index[0]]["title"]
            updater.bot.sendPhoto(id ,img, text, reply_markup = reply_markup)

            if len(self.question_list_index) > 0:
                self.question_list_index.pop(0)
        else:
            updater.bot.sendMessage(id, 'Bu mavzu bo\'yicha savollarimiz tugadi.')
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('✅testni tugatish', callback_data=f'✅ {pk} {user_id}'), InlineKeyboardButton('⬅️ortga', callback_data='⬅️ortga')]])
            updater.bot.sendMessage(id,'Yo\'nalishni tanlang',reply_markup=reply_markup)

    def add_option(self, update:Update, context:CallbackContext):
        quer = update.callback_query        
        q_id = quer.data.split()[1]
        o_id = quer.data.split()[2]
        r_id = quer.data.split()[3]
        pk = quer.data.split()[4]
        url = f"{b_url}/api/result_detail/"
        """xato bajardim vaqtinchalik result:1 dib"""
        r = requests.post(url=url, json={"result":r_id, "question":q_id, "option":o_id})
        data = r.json()
        url2 = f"{b_url}/api/result_detail/{data['option']}/"
        r2 = requests.get(url2)
        data2 = r2.json()
        if data2["is_correct"] == False:
            quer.edit_message_caption(caption="❌❌" + str(data2["is_correct"]) + "❌❌")
        if data2["is_correct"] == True:
            quer.edit_message_caption(caption="✅✅" + str(data2["is_correct"]) + "✅✅")

        self.quiston1(update, context, pk, r_id, quer.message.chat.id)

    def statestik(self, update:Update, context:CallbackContext):
        quer = update.callback_query
        s_id = quer.data.split()[-1]
        t_id = quer.data.split()[1]

        url = f"{b_url}/api/result/{s_id}/{t_id}"
        r = requests.get(url)
        data = r.json()
        text = f"✅ to'g'ri javoblar soni " + str(data['student']["results"][0]["score"])
        quer.edit_message_text(text, reply_markup=None)

updater = Updater(TOKEN)
bot_quiz = Quiz_bot()

updater.dispatcher.add_handler(CommandHandler('start', bot_quiz.start))
updater.dispatcher.add_handler(CommandHandler('quiz', bot_quiz.quiz))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.quer_start, pattern='⬅️ortga', ))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.topic, pattern='🥈⬅️ortga', ))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.topic, pattern='🥇'))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.border, pattern="📌🥈"))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.quitoin, pattern="🥈"))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.quiston1, pattern="⏩"))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.add_option, pattern="❔"))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.statestik, pattern="✅"))


#Start the bot
updater.start_polling()
updater.idle()