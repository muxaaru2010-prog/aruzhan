import telebot
import requests
from telebot import types

BOT_TOKEN = "8252107209:AAFDbgZRkM2n_HjVW-a6aXWzvPtyHih8MU8"
KEY = "af1ecbd4bfdc4754bcc93754250811"  

bot = telebot.TeleBot(BOT_TOKEN)
# --- Функция получения курса ---
def get_rate(currency):
    url = f"https://v6.exchangerate-api.com/v6/{KEY}/latest/{currency}"
    r = requests.get(url).json()
    # курс от выбранной валюты к тенге
    return r["conversion_rates"]["KZT"]

# --- Команда /start ---
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("USD 🇺🇸", "EUR 🇪🇺")
    markup.add("RUB 🇷🇺", "KGS 🇰🇬")
    bot.send_message(message.chat.id, "Выбери валюту:", reply_markup=markup)

# --- Обработка кнопок ---
@bot.message_handler(func=lambda m: True)
def buttons(message):
    text = message.text

    if "USD" in text:
        rate = get_rate("USD")
        bot.send_message(message.chat.id, f"1 USD = {rate} KZT")

    elif "EUR" in text:
        rate = get_rate("EUR")
        bot.send_message(message.chat.id, f"1 EUR = {rate} KZT")

    elif "RUB" in text:
        rate = get_rate("RUB")
        bot.send_message(message.chat.id, f"1 RUB = {rate} KZT")

    elif "KGS" in text:
        rate = get_rate("KGS")
        bot.send_message(message.chat.id, f"1 KGS = {rate} KZT")

    else:
        bot.send_message(message.chat.id, "Просто нажми кнопку валюты ")

bot.infinity_polling()

if __name__=='__main__':
 print("Бот запущен")
bot.polling(non_stop=True)
    