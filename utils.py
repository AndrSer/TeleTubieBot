import requests


class ConversionException(Exception):
    pass


class ResponseException(Exception):
    pass


class CurrenciesConverter:
    URL = 'https://www.cbr-xml-daily.ru/daily_json.js'

    @staticmethod
    def get_available_currencies():
        request_json = CurrenciesConverter.get_response()
        currencies = {request_json['Valute']['USD']['Name']: 'USD',
                      request_json['Valute']['EUR']['Name']: 'EUR',
                      'Рубль': 'RUB'}
        return currencies

    @staticmethod
    def get_daily_currencies():
        request_json = CurrenciesConverter.get_response()
        currencies = {request_json['Valute']['USD']['Name']: request_json['Valute']['USD']['Value'],
                      request_json['Valute']['EUR']['Name']: request_json['Valute']['EUR']['Value']}
        return currencies

    @staticmethod
    def get_response():
        response = requests.get(CurrenciesConverter.URL).json()

        if not response:
            raise ResponseException(f'Не удалось получить ответ от {CurrenciesConverter.URL}')
        return response

    @staticmethod
    def convert(quote: str, base: str, amount: str):
        request_json = CurrenciesConverter.get_response()
        result_convert = None

        if quote.strip().lower() == base.strip().lower():
            raise ConversionException('Валюты одинаковы. Невозможно сконвертировать одинаковые валюты.')

        currencies = CurrenciesConverter.get_available_currencies()

        if quote not in currencies.keys() or base not in currencies.keys():
            raise ConversionException('Валюты не в списке допустимых.')

        if base.strip().lower() == 'рубль':
            result_convert = float(request_json['Valute'][currencies[quote.strip()]]['Value']) * \
                             int(amount)
        elif quote.strip().lower() == 'рубль':
            result_convert = float(request_json['Valute'][currencies[quote.strip()]]['Value']) / \
                             int(amount)
        elif quote.strip().lower() != 'рубль' and base.strip().lower() != 'рубль':
            result_convert = float(request_json['Valute'][currencies[quote.strip()]]['Value']) / \
                             float(request_json['Valute'][currencies[base.strip()]]['Value']) * \
                             int(amount)
        return result_convert



