import config
import openai
import telebot

from message_store import MessageDataBase
from whitelist import Whitelist
from gpt_helper import GPTHelper


class GPTHandler:
    def __init__(self, message_store: MessageDataBase, whitelist: Whitelist, bot: telebot.TeleBot):
        openai.api_key = config.OPENAI_API_KEY

        self.message_store = message_store
        self.whitelist = whitelist
        self.bot = bot
        self.token_limit = 4096
        self.max_answer_tokens = 500
        self.max_context_tokens = self.token_limit - self.max_answer_tokens

    def handle_text(self, text: str, message: telebot.types.Message):
        self.message_store.store_message(text, message)

        if message.chat.type == 'group' and not message.text.startswith("/gpt"):
            return

        is_whitelist_user = self.whitelist.is_user_in_white_list(message)
        messages_amount = self.message_store.get_messages_amount_for_user_in_this_month(message)
        if messages_amount > config.FREE_MESSAGE_LIMIT and not is_whitelist_user:
            text = config.message_for_exceeded_limit()
            bot_message = self.bot.send_message(message.chat.id, text)
            self.message_store.store_message(text, bot_message)
            return

        response = openai.ChatCompletion.create(
            model=config.AI_MODEL,
            messages=self.get_context_messages(message.chat.id, message.chat.type),
            max_tokens=self.max_answer_tokens
        )

        # Send the response back to the user
        response_content = response['choices'][0]['message']['content']
        bot_message = self.bot.send_message(message.chat.id, response_content)
        self.message_store.store_message(bot_message.text, bot_message)

    def get_context_messages(self, chat_id: int, chat_type: str):
        if chat_type in ["group", "supergroup", "channel"]:
            system_message = config.group_system_message()
        else:
            system_message = config.private_chat_system_message()

        message_list = self.message_store.get_recent_messages(chat_id, 100)
        if system_message is not None:
            message_list.insert(0, system_message)

        while GPTHelper.num_tokens_from_messages(message_list) > self.max_context_tokens:
            message_list.pop(0)

        return message_list
