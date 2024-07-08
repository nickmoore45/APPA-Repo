import asyncio
from telegram import Bot
import os
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

async def send_telegram_message(bot_token, chat_id, message):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)


def send_message(text):
    bot_token = BOT_TOKEN
    chat_id = CHAT_ID
    asyncio.run(send_telegram_message(bot_token, chat_id, text))



