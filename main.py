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
    question_list_index = []
    def start(self, update:Update, context:CallbackContext):
        id = update.message.from_user.id
        url = f'{b_url}/quiz_list/'
        rq = requests.get(url)
        data_json = rq.json()

        url2 = f'{b_url}/users_list/'
        r2 = requests.get(url2)
        data_user = r2.json()

        first_name = update.message.from_user.first_name
        if not first_name:
            first_name = "Null"
        last_name = update.message.from_user.last_name
        if not last_name:
            last_name = 'Null'
        email = f"Null@gmial.com"
        password = update.message.from_user.id

        data = {'ferst_name':first_name, 'last_name':last_name, "email":email, 'password':password}

        list_pass = []
        for i in data_user["user_listis"]:
            list_pass.append(i["password"])
        if str(password) not in list_pass:
                url = f"{b_url}/create_user/"
                r = requests.post(url, json=data)
                r.json()

        inline_key = []
        for i in data_json:
            ed = i['id']
            inline_key.append([InlineKeyboardButton(i['title'], callback_data=f'🥇{ed}')])
        reply_markup = InlineKeyboardMarkup(inline_key)
        updater.bot.sendMessage(id, 'Fanlar ro\'yxati', reply_markup=reply_markup)
    
    def quer_start(self, update:Update, context:CallbackContext):
        quer = update.callback_query
        url = f'{b_url}/quiz_list/'
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
        url = f'{b_url}/topic_list/{pk}/'
        rq = requests.get(url)
        data_json = rq.json()

        inline_key = []
        for i in data_json['quiz']["topics"]:
            ed = i['id']
            inline_key.append([InlineKeyboardButton(i['t_name'], callback_data=f'🥈{ed}')])
        inline_key.append([InlineKeyboardButton('⬅️ortga', callback_data='⬅️ortga')])
        reply_markup = InlineKeyboardMarkup(inline_key)
        quer.edit_message_text("Mavzular ro'yxati:", reply_markup=None)
        quer.edit_message_reply_markup(reply_markup=reply_markup)

    def quitoin(self, update:Update, context:CallbackContext):
        quer = update.callback_query
        quer.edit_message_text("📌Savvollar:", reply_markup=None)
        pk = quer.data[1:]
        url1 = f'{b_url}/question_list/{pk}/'
        rq = requests.get(url1)
        data_quitoin:dict = rq.json()

        self.question_list_index = data_quitoin['topic']['question_index_list']

        if len(self.question_list_index) > 0:
            inline_key = []
            text = ''
            n = 1
            for optons in data_quitoin['topic']['questions'][self.question_list_index[0]]["optons"]:
                    q_id = optons["quetion"]
                    o_id = optons['id']
                    t_id = data_quitoin['topic']['questions'][self.question_list_index[0]]['topic_id']
                    if n == 1:
                        text += "\n\nA) " + optons["option"]
                        inline_key.append([InlineKeyboardButton('A', callback_data=f'❔{t_id}{q_id}{o_id}')])
                    elif n == 2:
                        text += "\n\nB) " + optons["option"]
                        inline_key.append([InlineKeyboardButton('B', callback_data=f'❔{t_id}{q_id}{o_id}')])
                    elif n == 3:
                        text += "\n\nC) " + optons["option"]
                        inline_key.append([InlineKeyboardButton('C', callback_data=f'❔{t_id}{q_id}{o_id}')])
                    elif n == 4:
                        text += "\n\nD) " + optons["option"]
                        inline_key.append([InlineKeyboardButton('D', callback_data=f'❔{t_id}{q_id}{o_id}')])
                    n += 1
            reply_markup = InlineKeyboardMarkup(inline_key)
            updater.bot.sendMessage(quer.message.chat.id, data_quitoin['topic']['questions'][self.question_list_index[0]]['question']+text, reply_markup=reply_markup)
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('⏩kiying test', callback_data=f'⏩{pk}') ,InlineKeyboardButton('✅testni tugatish', callback_data='✅'), InlineKeyboardButton('⬅️ortga', callback_data='⬅️ortga')]])
            updater.bot.sendMessage(quer.message.chat.id,'Yo\'nalishni tanlang',reply_markup=reply_markup)
            if len(self.question_list_index) > 0:
                self.question_list_index.pop(0)
        else:
            updater.bot.sendMessage(quer.message.chat.id, 'Bu mavzu bo\'yicha savollarimiz tugadi.')
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('✅testni tugatish', callback_data='✅'), InlineKeyboardButton('⬅️ortga', callback_data='⬅️ortga')]])
            updater.bot.sendMessage(quer.message.chat.id,'Yo\'nalishni tanlang',reply_markup=reply_markup)

    def quiston1(self, update:Update, context:CallbackContext):
        quer = update.callback_query
        quer.edit_message_text("📌Savvollar:", reply_markup=None)
        pk = quer.data[1:]
        url1 = f'{b_url}/question_list/{pk}/'
        rq = requests.get(url1)
        data_quitoin:dict = rq.json()

        if len(self.question_list_index) > 0:
            inline_key = []
            text = ''
            n = 1
            for optons in data_quitoin['topic']['questions'][self.question_list_index[0]]["optons"]:
                    q_id = optons["quetion"]
                    o_id = optons['id']
                    t_id = data_quitoin['topic']['questions'][self.question_list_index[0]]['topic_id']
                    if n == 1:
                        text += "\n\nA) " + optons["option"]
                        inline_key.append([InlineKeyboardButton('A', callback_data=f'❔{t_id}{q_id}{o_id}')])
                    elif n == 2:
                        text += "\n\nB) " + optons["option"]
                        inline_key.append([InlineKeyboardButton('B', callback_data=f'❔{t_id}{q_id}{o_id}')])
                    elif n == 3:
                        text += "\n\nC) " + optons["option"]
                        inline_key.append([InlineKeyboardButton('C', callback_data=f'❔{t_id}{q_id}{o_id}')])
                    elif n == 4:
                        text += "\n\nD) " + optons["option"]
                        inline_key.append([InlineKeyboardButton('D', callback_data=f'❔{t_id}{q_id}{o_id}')])
                    n += 1
            reply_markup = InlineKeyboardMarkup(inline_key)
            updater.bot.sendMessage(quer.message.chat.id, data_quitoin['topic']['questions'][self.question_list_index[0]]['question']+text, reply_markup=reply_markup)
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('⏩kiying test', callback_data=f'⏩{pk}') ,InlineKeyboardButton('✅testni tugatish', callback_data='✅'), InlineKeyboardButton('⬅️ortga', callback_data='⬅️ortga')]])
            updater.bot.sendMessage(quer.message.chat.id,'Yo\'nalishni tanlang',reply_markup=reply_markup)
            if len(self.question_list_index) > 0:
                self.question_list_index.pop(0)
        else:
            updater.bot.sendMessage(quer.message.chat.id, 'Bu mavzu bo\'yicha savollarimiz tugadi.')
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('✅testni tugatish', callback_data='✅'), InlineKeyboardButton('⬅️ortga', callback_data='⬅️ortga')]])
            updater.bot.sendMessage(quer.message.chat.id,'Yo\'nalishni tanlang',reply_markup=reply_markup)


    def statest(self, update:Update, context:CallbackContext):
        quir = update.callback_query
        data = quir.data
        t_id = data[1]
        q_id = data[2]
        o_id = data[-1]
        url = f'{b_url}/question_list/{t_id}/'
        r = requests.get(url)
        r_json = r.json()

        url2 = f'{b_url}/users_list/'
        r2 = requests.get(url2)
        data_user = r2.json()

        for i in data_user["user_listis"]:
            if i['password'] == str(quir.message.chat.id):
                user_id = i['id']
        topisc_id = r_json['topic']['id']
        question_id = data[-1]

        data3 = {"user_id":user_id,"quiz_title":question_id, 'topic_name':topisc_id}
        url3 = f"{b_url}/create_result/"
        r3 = requests.post(url3, json=data3)

        result_id = r3.json()['id']

        url5 = f"{b_url}/option_chict/{o_id}/"
        r5 = requests.get(url5)
        o_chict = r5.json()['chict']

        url4 = f'{b_url}/create_result_detail/'
        r4 = requests.post(url4, json={"user":user_id, "result":result_id, "question_name":q_id, "is_solved":o_chict})
        r4_json = r4.json()
        r_detail_id = r4_json['result']

        url6 = f"{b_url}/chict_all/{user_id}/{r_detail_id}"
        r6 = requests.get(url6)
        r6_json = r6.json()
        self.true += r6_json['True']
        self.false += r6_json['False']

        quir.edit_message_reply_markup(reply_markup=None)

    def stop(self, update:Update, context:CallbackContext):
        quir = update.callback_query
        quir.edit_message_text(f'statestika:', reply_markup=None)
        updater.bot.sendMessage(quir.message.chat.id, f"to'gri:{self.true} / xato:{self.false}")
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('⬅️boshminu', callback_data='⬅️ortga')]])
        updater.bot.sendMessage(quir.message.chat.id,"👇bosh minu👇",reply_markup=reply_markup)
        self.true = 0
        self.false = 0

updater = Updater(TOKEN)
bot_quiz = Quiz_bot()

updater.dispatcher.add_handler(CommandHandler('start', bot_quiz.start))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.quer_start, pattern='⬅️ortga', ))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.topic, pattern='🥈⬅️ortga', ))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.topic, pattern='🥇'))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.quitoin, pattern="🥈"))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.quiston1, pattern="⏩"))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.statest, pattern='❔'))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.stop, pattern="✅"))


#Start the bot
updater.start_polling()
updater.idle()