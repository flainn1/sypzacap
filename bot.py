import random
import string
import telebot
from telebot import types
import time

API_TOKEN = '7579343898:AAEYznuehrWFL2y3VH0fegKAoAF6o3rTqIU'
CHANNEL_LINK = 'https://t.me/+q0Kg9zjN1TtjNGRi'
SUCCESS_GIF_URL = 'https://media1.tenor.com/m/nlcD6WDDoDsAAAAd/kenshin.gif'

bot = telebot.TeleBot(API_TOKEN)

def generate_captcha():
    return ''.join(random.choices(string.ascii_lowercase, k=5))

@bot.message_handler(commands=['start'])
def start(message):
    captcha_word = generate_captcha()
    
    options = [generate_captcha() for _ in range(5)]
    correct_position = random.randint(0, 5)
    options.insert(correct_position, captcha_word)
    
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    
    for option in options:
        callback_data = 'captcha_solved' if option == captcha_word else 'wrong'
        keyboard.add(types.InlineKeyboardButton(option, callback_data=callback_data))
    
    bot.send_message(
        message.chat.id,
        f"👋 Привет! Чтобы получить доступ к каналу, реши капчу: {captcha_word}",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'captcha_solved':
        bot.send_animation(chat_id=call.message.chat.id, animation=SUCCESS_GIF_URL)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="✅ Капча пройдена! Твоя ссылка: " + CHANNEL_LINK
        )
    else:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="❌ Неверно! Попробуйте снова."
        )

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            time.sleep(5)  # Подождите 5 секунд перед повторной попыткой
