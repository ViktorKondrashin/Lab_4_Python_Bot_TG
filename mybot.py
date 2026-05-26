import configparser
import telebot
from telebot import types
from pycoingecko import CoinGeckoAPI

config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")

bot_token = config["telegram"]["token"]

bot = telebot.TeleBot(bot_token)

cg = CoinGeckoAPI()

def main_keyboard():
    """Клавиатура главного меню."""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Получить курс биткоина"))
    return keyboard


def back_keyboard():
    """Клавиатура после показа курса."""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Перейти на главную"))
    return keyboard


def show_main_menu(message):
    """Показывает главное меню."""
    bot.send_message(
        message.chat.id,
        "Мы на главной. Выбери действие:",
        reply_markup=main_keyboard()
    )

def send_bitcoin_price(message):
    price = cg.get_price(ids="bitcoin", vs_currencies="usd")

    bot.send_message(
        message.chat.id,
        f'Bitcoin Price: {price["bitcoin"]["usd"]}$',
        reply_markup=back_keyboard()
    )

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        f"Здравствуйте, {message.from_user.first_name}!"
    )

    bot.send_message(
        message.chat.id,
        "Чтобы перейти на главную, нажми кнопку или введи /crypto.",
        reply_markup=back_keyboard()
    )


@bot.message_handler(commands=["crypto"])
def crypto_command(message):
    show_main_menu(message)


@bot.message_handler(func=lambda message: message.text == "Перейти на главную")
def go_to_main(message):
    show_main_menu(message)


@bot.message_handler(func=lambda message: message.text == "Получить курс биткоина")
def go_to_bitcoin_price(message):
    send_bitcoin_price(message)

@bot.message_handler(commands=['bitcoin'])
def send_bitcoin_command(message):
    send_bitcoin_price(message)

@bot.message_handler(commands=['help'])
def help_command(message):

    help_text = (
        "Справка по боту:\n\n"
        "Команды:\n"
        "/start — начать работу с ботом\n"
        "/crypto — открыть главное меню\n"
        "/bitcoin — получить курс Bitcoin\n"
        "/help — показать справку\n\n"
        "Кнопки:\n"
        "Получить курс биткоина — получить текущий курс Bitcoin в долларах\n"
        "Перейти на главную — вернуться в главное меню"
    )

    bot.send_message(message.chat.id, help_text, reply_markup=back_keyboard())

bot.polling()