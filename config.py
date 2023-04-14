TELEGRAM_API_KEY = ""
OPENAI_API_KEY = ""

ADMIN_USERNAME = ""
BOT_USERNAME = ""

FREE_MESSAGE_LIMIT = 20
AI_MODEL = "gpt-3.5-turbo-0301"

DB_FILENAME = "database.db"
AUDIOS_DIR = "audios"


def message_for_exceeded_limit():
    return (f"You have reached the limit of {FREE_MESSAGE_LIMIT} messages for this month. "
            f"To continue using this service, please contact @{ADMIN_USERNAME} for assistance. "
            "Thank you for understanding.")


def welcome_message():
    return ("Welcome to ChatGPT Bot! 🤖\n\n"
            f"Please note that this is not an official bot, but it uses the official GPT API ({AI_MODEL}).\n\n"
            f"As a trial, you can send up to {FREE_MESSAGE_LIMIT} messages for free this month. "
            f"If you want to use the bot more often, please contact @{ADMIN_USERNAME} for assistance. "
            "Enjoy chatting with the AI!")


def group_system_message():
    return {
        "role": "system",
        "content": "You are a helpful assistant in a group chat. There are a lot of people in the chat room, "
                   "you can identify them by their name at the beginning of each message in []. But you don't "
                   "have to put your name at the beginning, answer as usual."
    }


def private_chat_system_message():
    return {
        "role": "system",
        "content": "You are a helpful assistant in a private chat. Please feel free to ask any questions."
    }
