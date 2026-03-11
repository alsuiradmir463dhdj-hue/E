import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os

SESSION_STRING = os.environ.get('SESSION_STRING')
API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if "рынка" in event.message.message.lower():
        await event.reply("Отправляй подарок! 🎁")

async def main():
    await client.start()
    print("Бот запущен!")
    await client.run_until_disconnected()

asyncio.run(main())
