import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

API_TOKEN = '7579343898:AAEYznuehrWFL2y3VH0fegKAoAF6o3rTqIU'
CHANNEL_LINK = 'https://t.me/+ScVpIXp3cYpkMjcy'

def start(update: Update, context: CallbackContext) -> None:
    captcha_word = ''.join(random.choices(string.ascii_lowercase, k=5))
    context.user_data['captcha'] = captcha_word
    keyboard = [
        [InlineKeyboardButton(captcha_word, callback_data='captcha_solved')],
        [InlineKeyboardButton('1', callback_data='wrong'),
         InlineKeyboardButton('2', callback_data='wrong'),
         InlineKeyboardButton('3', callback_data='wrong'),
         InlineKeyboardButton('4', callback_data='wrong'),
         InlineKeyboardButton('5', callback_data='wrong'),
         InlineKeyboardButton('6', callback_data='wrong')]
    ]
    update.message.reply_text(
        f"👋 Привет! Чтобы получить доступ к каналу, реши капчу: {captcha_word}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if query.data == 'captcha_solved':
        query.edit_message_text(text="✅ Капча пройдена! Вот ссылка на канал: " + CHANNEL_LINK)
    else:
        query.edit_message_text(text="❌ Неверно! Попробуйте снова.")

def main() -> None:
    updater = Updater(API_TOKEN)
    
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    