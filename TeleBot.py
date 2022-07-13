import utils
import telebot
import re


def get_config(path: str):
    config = {}
    config_file = open(path)
    for line in config_file:
        config[re.split('=', line)[0].replace(' ', '')] = re.split('=', line)[1].replace(' ', '')
    return config


bot = telebot.TeleBot(get_config('config.cfg').get('TOKEN'))


# def echo_test(message: telebot.types.Message):
#     bot.send_message(message.chat.id, 'Добрый день!')


@bot.message_handler(commands=['start', 'help'])
def start_help_message(message: telebot.types.Message):
    text_message = 'Чтобы начать работу введите команду в следующем формате:\n<Имя валюты>, \
                   <В какую валюту перевести>, \
                   <Количество переводимой валюты>\n \
                   Имя валюты должно совпадать с именем доступных валют. Пример:\n \
                   Доллар США, Рубль, 200\n \
                   Для получения списка доступных валют введите /values\n \
                   Для получения текущего курса введите /daily'
    bot.reply_to(message, text_message)


@bot.message_handler(commands=['values'])
def output_values_currencies(message: telebot.types.Message):
    text_message = 'Доступные для перевода валюты:\n'
    currencies = utils.CurrenciesConverter.get_available_currencies()
    text_message += '\n'.join(currencies.keys())
    bot.reply_to(message, text_message)


@bot.message_handler(commands=['daily'])
def daily_currencies(message: telebot.types.Message):
    text_message = 'Текущий курс доступных валют:\n'
    currencies = utils.CurrenciesConverter.get_daily_currencies()
    text_message += '\n'.join(currencies.keys()).join(' -> ').join(currencies.values())
    bot.reply_to(message, text_message)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        if not re.fullmatch("^\\w+\\s\\w+, \\w+, \\d+$|^\\w+, \\w+, \\d+$|^\\w+, \\w+\\s\\w+, \\d+$", message.text):
            raise utils.ConversionException('Формат строки не совпадает с необходимым.')
        parse_response = message.text.split(', ')
        result_convert = utils.CurrenciesConverter.convert(parse_response[0], parse_response[1], parse_response[2])
    except utils.ConversionException as e:
        bot.reply_to(message, f'Ошибка конвертирования\n {e}')
    except utils.ResponseException as e:
        bot.reply_to(message, f'Ошибка получения курса валют\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n {e}')
    else:
        text = f"""Сконвертировано:
                       {parse_response[0].strip()} в {parse_response[1].strip()} с количеством {parse_response[2].strip()}
                       {str(round(result_convert, 2))}"""
        bot.send_message(message.chat.id, text)


bot.polling()
