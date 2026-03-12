import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os

# ========== КОНФИГУРАЦИЯ ==========
SESSION_STRING = os.environ.get('SESSION_STRING')
API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')

print("🔑 Длина SESSION_STRING:", len(SESSION_STRING) if SESSION_STRING else "None")
print("📊 Первые 50 символов:", SESSION_STRING[:50] if SESSION_STRING else "None")

try:
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    print("✅ Клиент создан")
except Exception as e:
    print(f"❌ Ошибка создания клиента: {e}")
    exit(1)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.message.message and "рынка" in event.message.message.lower():
        await event.reply("Отправляй подарок! 🎁")
        print(f"✅ Ответил {event.sender_id}")

async def main():
    await client.start()
    me = await client.get_me()
    print(f"✅ Успешный вход! Аккаунт: @{me.username}")
    print("🤖 Бот слушает сообщения...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())