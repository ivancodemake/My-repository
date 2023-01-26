import telebot
from config import TOKEN, currency
from extensions import APIException, Converter
import time


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def greet(message: telebot.types.Message):
    text_greet = "Вас приветствует бот-конвертер валют!"
    bot.send_message(message.chat.id, text_greet)

    time.sleep(2)

    text_rule = 'Для начала конвертации введите данные в следующем формате:\n<имя валюты><в какую валюту перевести>\
    <количество переводимой валюты>\nПример ввода: евро доллар 100'
    bot.send_message(message.chat.id, text_rule)

    time.sleep(4)

    text_option = "Список доступных валют: /values"
    bot.send_message(message.chat.id, text_option)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in currency.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values_2 = message.text.split()

        if len(values_2) != 3:
            raise APIException('Неверный формат ввода!')

        quote, base, amount = values_2
        amount = amount.replace(',', '.')
        total_base = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя!\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        price = total_base*float(amount)
        text = f'Цена {amount} {quote} в {base} - {round(price, 2)}'
        bot.send_message(message.chat.id, text)


bot.polling(non_stop=True)

