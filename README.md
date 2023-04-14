# ChatGPT Telegram Bot

This project is a Telegram bot that allows users to communicate with OpenAI's ChatGPT. It is built using Python and the Telebot library. The bot provides helpful assistance in both private and group chats, with a free message limit per user per month. To continue using the service beyond this limit, users can contact the admin for assistance.

## Features

- Private and group chat support
- Free message limit per user per month
- Admin controlled whitelist for extended usage
- Text and voice message support
- SQLite database for message storage and user management
- GPT-4 support for better response quality

## Installation and Setup

1. Clone the repository:
```
git clone https://github.com/yourusername/ChatGPT-Telegram-Bot.git
cd ChatGPT-Telegram-Bot
```
2. Install the required dependencies:
```
pip install -r requirements.txt
```
3. Set up the API keys and other configurations in the `config.py` file:

- `TELEGRAM_API_KEY`: Your Telegram API key obtained from the BotFather.
- `OPENAI_API_KEY`: Your OpenAI API key.
- `ADMIN_USERNAME`: Your Telegram username (without the @ symbol).
- `BOT_USERNAME`: Your bot's username (without the @ symbol).
- `FREE_MESSAGE_LIMIT`: The free message limit per user per month.
- `AI_MODEL`: The GPT model to use (e.g., `gpt-3.5-turbo-0301`).
- `DB_FILENAME`: The SQLite database filename (e.g., `database.db`).
- `AUDIOS_DIR`: The directory to store audio files for voice message processing.

4. Run the bot:
```
python bot.py
```

## Running the bot as a service

You can also set up the ChatGPT bot to run as a service on your server. This allows the bot to start automatically when the server boots and remain running in the background. More detailed instructions on how to achieve this will be dependent on your server's operating system and configuration. Please consult the relevant documentation for your specific environment.


## Usage

Start a conversation with the bot by searching for its username in Telegram. Send `/start` to receive a welcome message and instructions on how to use the bot. You can start asking questions or having a conversation with the AI.

In group chats, use the `/gpt` command to send a message to the bot, for example:

`/gpt What is the capital of France?`


To add a user to the whitelist, the admin can use the `/whitelist` command followed by the user ID:

`/whitelist 123456789`


## Contributing

Pull requests and contributions are welcome. Please open an issue to discuss any changes or improvements you would like to propose.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This is not an official bot, but it uses the official GPT API. The developers of this project are not responsible for any misuse or violation of OpenAI's terms of service.
