from telebot import TeleBot
import time

bot = TeleBot("8252107209:AAFDbgZRkM2n_HjVW-a6aXWzvPtyHih8MU8")
total = 0
water_norm = 2500
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Я бот для отслеживания воды "
    )
    
@bot.message_handler(commands=['setreminder'])
def reminder_message(message):
    bot.send_message(message.chat.id, "Напомню через 2 часа ")
    time.sleep(2 * 60 * 60)
    bot.send_message(message.chat.id, " Пора пить воду!")


@bot.message_handler(commands=['add'])
def add_message(message):
    global total
    try:
        amount = int(message.text.split()[1])
        total += amount
        bot.send_message(
            message.chat.id,
            f"Выпито {amount} мл \nВсего: {total} мл"
        )
    except:
        bot.send_message(
            message.chat.id,
            "Ошибка \nИспользуй команду так:\n/add 250"
        )

@bot.message_handler(commands=['total'])
def total_message(message):
    bot.send_message(message.chat.id, f"Всего выпито: {total} мл ")

@bot.message_handler(commands=['status'])
def status_message(message):
    if total >= water_norm:
        bot.send_message(
            message.chat.id,
            "Норма воды выполнена! Молодец!"
        )
    else:
        bot.send_message(
            message.chat.id,
            f"&#9888; Норма воды не выполнена.\n"
            f"Осталось выпить {water_norm - total} мл"
        )
@bot.message_handler(commands=['endday'])
def endday_message(message):
    global total
    if total >= water_norm:
        bot.send_message(
            message.chat.id,
            " Итог дня:\nНорма воды выполнена! Отличная работа "
        )
    else:
        bot.send_message(
            message.chat.id,
            f" Итог дня:\n"
            f"Норма воды не выполнена.\n"
            f"Не хватило {water_norm - total} мл"
        )
    total = 0 
print("Бот работает")
bot.infinity_polling()
    
