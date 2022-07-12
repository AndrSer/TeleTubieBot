import requests
import telebot
import re


class ConversionException(Exception):
    pass


class ResponseException(Exception):
    pass


TOKEN = '5574715306:AAHKxR40lX5pPMTpfqarqTd8K_91vJ7_3uc'
URL = 'https://www.cbr-xml-daily.ru/daily_json.js'
bot = telebot.TeleBot(TOKEN)


def get_response(inner_url: str):
    response = requests.get(inner_url).json()
    if not response:
        raise ResponseException(f'Не удалось получить ответ от {inner_url}')
    return response


main_request_json = get_response(URL)
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
    if not re.fullmatch("^\\w+\\s\\w+, \\w+, \\d+$|^\\w+, \\w+, \\d+$|^\\w+, \\w+\\s\\w+, \\d+$", message.text):
        raise ConversionException('Формат строки не совпадает с необходимым.')
    parse_response = message.text.split(', ')

    if parse_response[0].strip().lower() == parse_response[1].strip().lower():
        raise ConversionException('Валюты одинаковы. Невозможно сконвертировать одинаковые валюты.')

    request_json = get_response(URL)
    if parse_response[0] not in currencies.keys() or parse_response[1] not in currencies.keys():
        raise ConversionException('Валюты не в списке допустимых.')
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
    text = f"""Сконвертировано:
               {parse_response[0].strip()} в {parse_response[1].strip()} с количеством {parse_response[2].strip()}
               {str(round(result_convert, 2))}"""
    bot.send_message(message.chat.id, text)


bot.polling()
