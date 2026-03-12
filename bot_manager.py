import asyncio
from telethon import TelegramClient, events
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
ACCESS_CODE = "8532"

bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("🔐 **Введите код доступа:**")

@bot.on(events.NewMessage)
async def handler(event):
    text = event.message.message.strip()
    if text == ACCESS_CODE:
        await event.reply("✅ **Код верный! Доступ разрешён.**")
    elif "я с рынка" in text.lower():
        await event.reply("Отправляй подарок! 🎁")

async def main():
    me = await bot.get_me()
    logger.info(f"✅ Бот @{me.username} запущен!")
    logger.info(f"🔐 Код доступа: {ACCESS_CODE}")
    await bot.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
