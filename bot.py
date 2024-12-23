import random
import string
import telebot
from telebot import types

API_TOKEN = '7579343898:AAEYznuehrWFL2y3VH0fegKAoAF6o3rTqIU'
CHANNEL_LINK = 'https://t.me/+ScVpIXp3cYpkMjcy'
SUCCESS_GIF_URL = 'https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExMWNoa2ZtczZjN3JxcnAybzlybXBidWsxbzJ5azNjY3c4aGR0aG83MCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/OjjOPhVoalJLO/giphy.webp'  # Replace with your desired GIF URL

bot = telebot.TeleBot(API_TOKEN)

def generate_captcha():
    return ''.join(random.choices(string.ascii_lowercase, k=5))

@bot.message_handler(commands=['start'])
def start(message):
    captcha_word = generate_captcha()
    keyboard = types.InlineKeyboardMarkup(row_width=3) 
    
    keyboard.add(types.InlineKeyboardButton(captcha_word, callback_data='captcha_solved'))
    
    for _ in range(5):  
        random_word = generate_captcha()
        keyboard.add(types.InlineKeyboardButton(random_word, callback_data='wrong'))
    
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
        bot.send_animation(
            chat_id=call.message.chat.id,
            animation=SUCCESS_GIF_URL 
        )
    else:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="❌ Неверно! Попробуйте снова."
        )

if __name__ == '__main__':
    bot.polling(none_stop=True)
