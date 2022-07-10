import requests
import telebot

TOKEN = '5574715306:AAHKxR40lX5pPMTpfqarqTd8K_91vJ7_3uc'
bot = telebot.TeleBot(TOKEN)
currencies = {
    'Американский доллар': 'USD',
    'Евро': 'EUR'
}


# def echo_test(message: telebot.types.Message):
#     bot.send_message(message.chat.id, 'Добрый день!')


@bot.message_handler(commands=['start', 'help'])
def start_help_message(message: telebot.types.Message):
    text_message = 'Чтобы начать работу введите команду в следующем формате:\n<Имя валюты> \
                   <В какую валюту перевести> \
                   <Количество переводимой валюты>'
    bot.reply_to(message, text_message)


@bot.message_handler(commands=['values'])
def output_values_currencies(message: telebot.types.Message):
    text_message = 'Доступные для перевода валюты:\n'
    text_message += '\n'.join(currencies.keys())
    bot.reply_to(message, text_message)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    parse_response = message.text.split(' ')
    request_json = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    result_convert = ''

    if parse_response[1].lower() == 'рубль':
        result_convert = str(float(request_json['Valute'][currencies[parse_response[0]]]['Value']) *
                             float(parse_response[2]))
    elif parse_response[0].lower() == 'рубль':
        result_convert = str(
            float(request_json['Valute'][currencies[parse_response[0]]]['Value']) /
            float(parse_response[2]))


bot.polling()
