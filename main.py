from telegram.ext import Updater,MessageHandler,Filters,CallbackContext,CommandHandler,CallbackQueryHandler,StringCommandHandler
from telegram import Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
import requests
import json

TOKEN = '5677023630:AAGdskZAvZwdRix213Ho28QaN-NZVcQtuU8'
class Quiz_bot:
    def start(self, update:Update, context:CallbackContext):
        id = update.message.from_user.id
        url = 'http://127.0.0.1:8000/quiz_list/'
        rq = requests.get(url)
        data_json = rq.json()

        inline_key = []
        for i in data_json:
            ed = i['id']
            inline_key.append([InlineKeyboardButton(i['title'], callback_data=f'🥇{ed}')])
        inline_key.append([InlineKeyboardButton('⬅️ortga', callback_data='⬅️ortga')])
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
        inline_key.append([InlineKeyboardButton('⬅️ortga', callback_data='⬅️ortga')])
        reply_markup = InlineKeyboardMarkup(inline_key)
        quer.edit_message_text("Fanlar ro\'yxati", reply_markup=None)
        quer.edit_message_reply_markup(reply_markup=reply_markup)

    def topic(self, update:Update, context:CallbackContext):
        quer = update.callback_query
        data_json_2 = []
        inline_key = [[InlineKeyboardButton("Print()1", callback_data=f'🥈{1}')], [InlineKeyboardButton("Print()1", callback_data=f'🥈{1}')], [InlineKeyboardButton("Print()3", callback_data=f'🥈{1}')]]
        for i in data_json_2:
            inline_key.append([InlineKeyboardButton(i['p_name'], callback_data=f'🥈{i[id]}')])
        inline_key.append([InlineKeyboardButton('⬅️ortga', callback_data='⬅️ortga')])
        reply_markup = InlineKeyboardMarkup(inline_key)
        quer.edit_message_text('Mavzular ro\'yhati:', reply_markup=None)
        quer.edit_message_reply_markup(reply_markup=reply_markup)

    def quitoin(self, update:Update, context:CallbackContext):
        quer = update.callback_query
        data_json_2 = []
        inline_key = [[InlineKeyboardButton("Print() nima1", callback_data=f'topic_id={1}')], [InlineKeyboardButton("Print()nima2", callback_data=f'topic_id={1}')], [InlineKeyboardButton("Print() nima 3", callback_data=f'topic_id={1}')]]
        for i in data_json_2:
            inline_key.append([InlineKeyboardButton(i['p_name'], callback_data=f'topic_id={i[id]}')])
        inline_key.append([InlineKeyboardButton('⬅️ortga', callback_data='🥈⬅️ortga')])
        for i in inline_key:
            reply_markup = InlineKeyboardMarkup(inline_key)
            quer.edit_message_text('Mavzular ro\'yhati:', reply_markup=None)
            quer.edit_message_reply_markup(reply_markup=reply_markup)

        


updater = Updater(TOKEN)
bot_quiz = Quiz_bot()

updater.dispatcher.add_handler(CommandHandler('start', bot_quiz.start))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.quer_start, pattern='⬅️ortga', ))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.topic, pattern='🥈⬅️ortga', ))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.topic, pattern='🥇'))
updater.dispatcher.add_handler(CallbackQueryHandler(bot_quiz.quitoin, pattern="🥈"))


#Start the bot
updater.start_polling()
updater.idle()