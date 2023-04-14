import config
import telebot

from telebot.apihelper import ApiTelegramException
from whitelist import Whitelist
from utility import Utility


class UserHandler:
    def __init__(self, whitelist: Whitelist, bot: telebot.TeleBot):
        self.whitelist = whitelist
        self.bot = bot

    def send_welcome_message(self, chat_id: int):
        self.bot.send_message(chat_id, config.welcome_message())

    def try_add_user_to_whitelist(self, message: telebot.types.Message):
        if message.from_user.username == config.ADMIN_USERNAME:
            user_id = Utility.extract_user_id(message.text)
            if user_id:
                self.whitelist.add_user_to_whitelist(user_id)
                try:
                    self.bot.send_message(user_id, "You have been added to the whitelist.")
                    self.bot.send_message(message.chat.id, f"User {user_id} has been added to the whitelist.")
                except ApiTelegramException as e:
                    if e.error_code == 400 and "chat not found" in e.description:
                        self.bot.send_message(message.chat.id, "Failed to notify the user. The user may have to start a chat with the bot first.")
                    else:
                        self.bot.send_message(message.chat.id, "An error occurred while sending the message.")
            else:
                self.bot.send_message(message.chat.id, "Please provide a valid user ID: /whitelist user_id")
        else:
            self.bot.send_message(message.chat.id, "You don't have permission to perform this action.")
