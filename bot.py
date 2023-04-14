import telebot
import logging
import config

from message_store import MessageDataBase
from whitelist import Whitelist
from voice_recogniser import VoiceRecogniser
from gpt_handler import GPTHandler
from user_handler import UserHandler

message_store = MessageDataBase(config.DB_FILENAME)
whitelist = Whitelist(config.DB_FILENAME)
bot = telebot.TeleBot(config.TELEGRAM_API_KEY)
voice_recogniser = VoiceRecogniser(bot)
gpt_handler = GPTHandler(message_store, whitelist, bot)
user_handler = UserHandler(whitelist, bot)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    user_handler.send_welcome_message(message.chat.id)


@bot.message_handler(commands=['whitelist'])
def whitelist_user(message: telebot.types.Message):
    user_handler.try_add_user_to_whitelist(message)


@bot.message_handler(content_types=['text'])
def handle_message(message: telebot.types.Message):
    gpt_handler.handle_text(message.text, message)


@bot.message_handler(content_types=['voice'])
def handle_voice(message: telebot.types.Message):
    text = voice_recogniser.covert_voice_to_text(message)
    gpt_handler.handle_text(text, message)


# Start the bot
bot.polling()
