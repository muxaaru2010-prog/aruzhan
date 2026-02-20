import telebot
import requests

TELEGRAM_BOT_TOKEN = '7479307259:AAHBLWSpInY81zmgxny4u5Y6dl8ddOrD8Xs'
WEATHER_API_KEY = '7479307259:AAHBLWSpInY81zmgxny4u5Y6dl8ddOrD8Xs'

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


def get_weather(city):
    try:
        url = f'https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q{city}&lang=ru'
        response = requests.get(url)
        data = response.json()
        
        if 'error' not in data:
            location = data['location']['name']
            country = data['location']['country']
            current = data['current']
            weather_des = current['condition']['text']
            temp = current['temp_c']
            humidity = current['humidity']
            wind_speed = current['wind_kph']
            weather_report = (
                f'Current weather in {location},{country}:\n'
                f'Description:{'weather_desc'}\n'
                f'Temperature:{temp} C \n'
                f'Humidity:{humidity}\n'
                f'Wind speed:{wind_speed}\n'
            )
        else:
            weather_report = f'Error: {data['error']['message']}'
    except requests.exceptions.RequestsException:
        weather_report = 'Error: Can not report weather '
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Здравствуйте  я бот для погоды напишите мне город я напишу вам текущую погоду города ')
@bot.message_handler(func=lambda message:True)
def send_weather(message):
    city = message.text.strip()
    weather = get_weather(city)
    bot.reply_to(message.weather)
        