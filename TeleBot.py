import requests
import telebot

TOKEN = '5574715306:AAHKxR40lX5pPMTpfqarqTd8K_91vJ7_3uc'
bot = telebot.TeleBot(TOKEN)

main_request_json = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
currencies = {main_request_json['Valute']['USD']['Name']: 'USD',
              main_request_json['Valute']['EUR']['Name']: 'EUR'}

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
    parse_response = message.text.split(', ')
    request_json = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    result_convert = None

    if parse_response[1].strip().lower() == 'рубль':
        result_convert = float(request_json['Valute'][currencies[parse_response[0].strip()]]['Value']) * \
                         int(parse_response[2])
    elif parse_response[0].strip().lower() == 'рубль':
        result_convert = float(request_json['Valute'][currencies[parse_response[0]].strip()]['Value']) / \
                         int(parse_response[2])
    elif parse_response[0].strip().lower() != 'рубль' and parse_response[1].strip().lower() != 'рубль':
        result_convert = float(request_json['Valute'][currencies[parse_response[0]].strip()]['Value']) / \
                         float(request_json['Valute'][currencies[parse_response[1]].strip()]['Value']) * \
                         int(parse_response[2])
    bot.send_message(message.chat.id, str(round(result_convert, 2)))


bot.polling()
