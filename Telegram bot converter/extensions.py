import requests
import json
from config import currency


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты "{base}".')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise APIException(f'Неверный ввод валюты "{quote}".')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise APIException(f'Неверный ввод валюты "{base}".')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Неверный ввод количества "{amount}".')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[currency[base]]

        return total_base
