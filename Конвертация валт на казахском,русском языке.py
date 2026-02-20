import telebot
import requests
from telebot import types

BOT_TOKEN = "8252107209:AAFDbgZRkM2n_HjVW-a6aXWzvPtyHih8MU8"
KEY = "af1ecbd4bfdc4754bcc93754250811"  

bot = telebot.TeleBot(BOT_TOKEN)
сurrencies = ['USD','EUR','RUR','KZT','CNY']
user_data={}
def get_exchange_rate(base_currency,target_currency):
    url = f"https://v6.exchangerate-api.com/v6/{KEY}/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    if response.status_code ==200:
        rates = data['conversion_rates']
        if target_currency in rates:
            return rates[target_currency]
        else:
            return None
    else:
        return None
   
@bot.message_handler(commands=["start","help"])
def start(message):
    bot.reply_to(message, 'Добро пожаловать в наш бот! Я помогу тебе кронвертировать валюты! для этого вызови команду /convert потом введи сумму')

@bot.message_handler(commands='convert')
def start_conversation(message):
    user_data[message.chat.id]={}
    bot.send_message(message.chat.id, 'Введите нужную сумму')
    bot.register(message,process_amount)
def process_amount(message):
    try:
        amount =float(message.text)
        user_data[message.chat.id]['amount']=amount
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for currency in сurrencies:
            markup.add(currency)
        bot.send_message(message.chat.id,'Выберите одну из валют ниже',reply_markup=markup)
        bot.register(message,process_base_currency)
    except ValueError:
        bot.reply_to(message,"Please enter a number")
        
@bot.message_handler(content_types=["text"])
def send_rate(message):
    code = message.text.upper()
    try:
        if code in ["USD", "EUR"]:
            rate = get_exchange_rate(code, "KZT")
            bot.send_message(message.chat.id, f" 1 {code} = {rate} KZT")
        else:
            bot.send_message(message.chat.id, " Я знаю только USD и EUR. Попробуй снова.")
    except:
        bot.send_message(message.chat.id, " Ошибка! Попробуй позже")


def process_base_currency(message):
    base_currency=message.text.upper()
    if base_currency in сurrencies:
        base_currency[message.chat.id]['base_currency']=base_currency
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for currency in сurrencies:
            markup.add(currency)
        bot.send_message(message.chat.id,'Выберите валюты в которую в хотите перевести ',reply_markup=markup)
        bot.register(message,process_target_currency)    
def process_target_currency(message):
    target_currency= message.text.upper()
    if target_currency in сurrencies:
        user_data[message.chat.id]['target_currency']=target_currency
        amount= user_data[message.chat.id]['amount']
        base_currency= user_data[message.chat.id]['base_currency']
        exchange_rate= get_exchange_rate(base_currency,target_currency)
        if exchange_rate:
            converted_amount=amount*exchange_rate
            bot.send_message(message.chat.id,f'{amount} {base_currency} в {converted_amount}{target_currency}')
        else:
            bot.send_message(message.chat.id,'ERROR')
            
    else:
        bot.reply_to(message,'ERROR')
        
@bot.message_handler(commands=["start"])       
def start(message):        
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)   
    con1 = types.KeyboardButton("доллар (USD)") 
    con2 = types.KeyboardButton("еуро (EUR)")
    markup.add(con1, con2)
    bot.send_message(message.chat.id, "Біздің ботқа қош келдің! Мен сізге валюталарды айырбастауға көмектесемін! Ол үшін /convert пайдаланыңыз, содан кейін соманы енгіңіз")
        
@bot.message_handler(content_types=["text"])
def send_rate(message):
    text = message.text
    if "доллар" in text:
        rate = get_exchange_rate("USD", "KZT")    
        bot.send_message(message.chat.id,f" 1 USD = {rate}") 
    elif "еуро" in text:
        rate = get_exchange_rate("EUR", "KZT")    
        bot.send_message(message.chat.id,f" 1 EUR = {rate}") 

@bot.message_handler(func=lambda message:True)
def echo_all(message):
    bot.reply_to(message,'UNKNOWN COMMAND')
if __name__=='__main__':
 print("Бот запущен")
bot.infinity_polling()