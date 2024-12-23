import random
import string
import telebot
from telebot import types

API_TOKEN = '7579343898:AAEYznuehrWFL2y3VH0fegKAoAF6o3rTqIU'
CHANNEL_LINK = 'https://t.me/+ScVpIXp3cYpkMjcy'

bot = telebot.TeleBot(API_TOKEN)

def generate_captcha():
    return ''.join(random.choices(string.ascii_lowercase, k=5))

@bot.message_handler(commands=['start'])
def start(message):
    captcha_word = generate_captcha()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(captcha_word, callback_data='captcha_solved'))
    for i in range(1, 7):
        keyboard.add(types.InlineKeyboardButton(str(i), callback_data='wrong'))
    
    bot.send_message(
        message.chat.id,
        f"👋 Привет! Чтобы получить доступ к каналу, реши капчу: {captcha_word}",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'captcha_solved':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="✅ Капча пройдена! Вот ссылка на канал: " + CHANNEL_LINK
        )
    else:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="❌ Неверно! Попробуйте снова."
        )

if __name__ == '__main__':
    bot.polling(none_stop=True)
