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
        updater.bot.sendMessage(id, 'Hush kelibsiz')

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
            inline_key.append([InlineKeyboardButton(i['title'], callback_data=f'🥈{ed}')])
        inline_key.append([InlineKeyboardButton('⬅️ortga', callback_data='⬅️ortga')])
        reply_markup = InlineKeyboardMarkup(inline_key)
        quer.edit_message_text("Mavzular ro'yxati:", reply_markup=None)
        quer.edit_message_reply_markup(reply_markup=reply_markup)

    def quitoin(self, update:Update, context:CallbackContext):
        quer = update.callback_query
        quer.edit_message_text("📌Savvollar:", reply_markup=None)
        pk = quer.data[1:]
        url1 = f'{b_url}/api/question/{pk}/'
        rq = requests.get(url1)
        data_quitoin = rq.json()

        self.question_list_index = data_quitoin['quiz']['topic']["questions_index"]

        if len(self.question_list_index) > 0:
            img = data_quitoin['quiz']['topic']['questions'][self.question_list_index[0]]["img"]

            
            inline_key = []
            for optons in data_quitoin['quiz']['topic']['questions'][self.question_list_index[0]]["options"]:
                    q_id = optons["question"]
                    o_id = optons['id']
                    inline_key.append([InlineKeyboardButton(optons["title"], callback_data=f"❔{q_id}{o_id}")])
                    
            reply_markup = InlineKeyboardMarkup(inline_key)
            text = data_quitoin['quiz']['topic']['questions'][self.question_list_index[0]]["title"]
            updater.bot.sendPhoto(quer.message.chat.id ,img, text, reply_markup = reply_markup)
            
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
        url1 = f'{b_url}/api/question/{pk}/'
        rq = requests.get(url1)
        data_quitoin = rq.json()

        if len(self.question_list_index) > 0:
            img = data_quitoin['quiz']['topic']['questions'][self.question_list_index[0]]["img"]

            
            inline_key = []
            for optons in data_quitoin['quiz']['topic']['questions'][self.question_list_index[0]]["options"]:
                    q_id = optons["question"]
                    o_id = optons['id']
                    inline_key.append([InlineKeyboardButton(optons["title"], callback_data=f"❔{q_id}{o_id}")])
                    
            reply_markup = InlineKeyboardMarkup(inline_key)
            text = data_quitoin['quiz']['topic']['questions'][self.question_list_index[0]]["title"]
            updater.bot.sendPhoto(quer.message.chat.id ,img, text, reply_markup = reply_markup)
            
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('⏩kiying test', callback_data=f'⏩{pk}') ,InlineKeyboardButton('✅testni tugatish', callback_data='✅'), InlineKeyboardButton('⬅️ortga', callback_data='⬅️ortga')]])
            updater.bot.sendMessage(quer.message.chat.id,'Yo\'nalishni tanlang',reply_markup=reply_markup)

            if len(self.question_list_index) > 0:
                self.question_list_index.pop(0)
        else:
            updater.bot.sendMessage(quer.message.chat.id, 'Bu mavzu bo\'yicha savollarimiz tugadi.')
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('✅testni tugatish', callback_data='✅'), InlineKeyboardButton('⬅️ortga', callback_data='⬅️ortga')]])
            updater.bot.sendMessage(quer.message.chat.id,'Yo\'nalishni tanlang',reply_markup=reply_markup)

updater = Updater(TOKEN)
bot_quiz = Quiz_bot()

updater.dispatcher.add_handler(CommandHandler('start', bot_quiz.start))
updater.dispatcher.add_handler(CommandHandler('quiz', bot_quiz.quiz))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.quer_start, pattern='⬅️ortga', ))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.topic, pattern='🥈⬅️ortga', ))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.topic, pattern='🥇'))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.quitoin, pattern="🥈"))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.quiston1, pattern="⏩"))


#Start the bot
updater.start_polling()
updater.idle()