from telegram.ext import Updater,MessageHandler,Filters,CallbackContext,CommandHandler,CallbackQueryHandler,StringCommandHandler
from telegram import Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
import requests
import json

TOKEN = '5677023630:AAGdskZAvZwdRix213Ho28QaN-NZVcQtuU8'
class Quiz_bot:
    t = 0
    f = 0
    def start(self, update:Update, context:CallbackContext):
        id = update.message.from_user.id
        url = 'http://127.0.0.1:8000/quiz_list/'
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
        url = 'http://127.0.0.1:8000/quiz_list/'
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
        url = f'http://127.0.0.1:8000/topic_list/{pk}/'
        rq = requests.get(url)
        data_json = rq.json()

        inline_key = []
        for i in data_json['topic']:
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
        url1 = f'http://127.0.0.1:8000/question_list/{pk}/'
        rq = requests.get(url1)
        data_quitoin:dict = rq.json()

        for k,v in data_quitoin.items():
            if k == 'question':
                for q in v:
                    pk = q['id']
                    url2 = f'http://127.0.0.1:8000/option_list/{pk}/'
                    rq = requests.get(url2)
                    data_opition = rq.json()
                    inline_key = []
                    n = 1
                    for e in data_opition['option']:
                        o_id = e['is_right']
                        inline_key.append([InlineKeyboardButton(f"{n}) " + e['option'], callback_data=f'❔{o_id}')])
                        n += 1
                    reply_markup = InlineKeyboardMarkup(inline_key)
                    updater.bot.sendMessage(quer.message.chat.id, q["quetion"]+"❔", reply_markup=reply_markup)
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('✅tugatush', callback_data='✅'), InlineKeyboardButton('⬅️ortga', callback_data='⬅️ortga')]])
        updater.bot.sendMessage(quer.message.chat.id,'yo\'nalish',reply_markup=reply_markup)

    def statest(self, update:Update, context:CallbackContext):
        quir = update.callback_query
        if quir.data[1:] == 'True':
            self.t += 1
        elif quir.data[1:] == 'False':
            self.f += 1
        quir.edit_message_reply_markup(reply_markup=None)

    def stop(self, update:Update, context:CallbackContext):
        quir = update.callback_query
        quir.edit_message_text(f'statestika:', reply_markup=None)
        updater.bot.sendMessage(quir.message.chat.id, f"to\'g\'ri:{self.t}/ xato:{self.f}")
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('⬅️boshminu', callback_data='⬅️ortga')]])
        updater.bot.sendMessage(quir.message.chat.id,"👇bosh minu👇",reply_markup=reply_markup)
        self.f = 0
        self.t = 0

        


updater = Updater(TOKEN)
bot_quiz = Quiz_bot()

updater.dispatcher.add_handler(CommandHandler('start', bot_quiz.start))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.quer_start, pattern='⬅️ortga', ))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.topic, pattern='🥈⬅️ortga', ))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.topic, pattern='🥇'))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.quitoin, pattern="🥈"))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.statest, pattern='❔'))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.stop, pattern="✅"))


#Start the bot
updater.start_polling()
updater.idle()