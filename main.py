import telebot
import requests

BOT_TOKEN = '5401879504:AAF-uKlp1WFvU0QxA_7IozY6Ht7bYIaV2Ug'
STRATZ_API_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdWJqZWN0IjoiZWE5MDAzYmUtOGRiNS00NmQ5LThjZDAtNGQ1MzA4ZmMyMTZlIiwiU3RlYW1JZCI6IjM5ODUxNTUzOCIsIm5iZiI6MTcwNzk1Njg1MCwiZXhwIjoxNzM5NDkyODUwLCJpYXQiOjE3MDc5NTY4NTAsImlzcyI6Imh0dHBzOi8vYXBpLnN0cmF0ei5jb20ifQ.QA5fPxq9Ufspi_o1Ku8CgvzcPBjG8ploTrEbICF91fg'
API_URL = 'https://api.stratz.com/api/v1/Hero'

bot = telebot.TeleBot(BOT_TOKEN)


def get_counterpicks(hero_name):
    headers = {'X-Requested-With': 'XMLHttpRequest'}
    params = {'name': hero_name, 'key': STRATZ_API_TOKEN}
    response = requests.get(API_URL + '/GetHeroMatchups', headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        counterpicks = data.get('heroMatchups')
        return counterpicks
    else:
        return None


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который может отправить тебе 3 контрпика героя из Dota 2. Просто отправь мне имя героя.")


@bot.message_handler(func=lambda message: True)
def get_hero_counterpicks(message):
    hero_name = message.text
    counterpicks = get_counterpicks(hero_name)
    if counterpicks:
        counterpicks_info = "\n".join([f"{cp['localizedHeroName']}: {cp['advantage']}%" for cp in counterpicks[:3]])
        response = f"Топ 3 контрпика для {hero_name}:\n{counterpicks_info}"
    else:
        response = f"Контрпики для героя {hero_name} отсутствуют или не доступны."
    bot.reply_to(message, response)


if __name__ == '__main__':
    bot.polling()
