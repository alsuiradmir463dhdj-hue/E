import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os
import json
import random
import string
from datetime import datetime

# ========== КОНФИГУРАЦИЯ ==========
SESSION_STRING = os.environ.get('SESSION_STRING')
API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')

# ========== ХРАНИЛИЩЕ ПОДАРКОВ ==========
gifts = {}  # {gift_id: {"name": "...", "from_user": id, "key": "...", "status": "stored"}}
user_gifts = {}  # {user_id: [gift_id, ...]}

# Генератор уникального ключа
def generate_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    message = event.message.message
    sender = await event.get_sender()
    user_id = sender.id
    
    # ===== АВТО-ОТВЕТ НА "Я С РЫНКА" =====
    if "я с рынка" in message.lower():
        await event.reply("Отправляй подарок! 🎁")
        return
    
    # ===== КОМАНДЫ =====
    if message.startswith("/mykeys"):
        await show_my_keys(event, user_id)
    
    elif message.startswith("/getgift"):
        await get_gift_by_key(event, message)
    
    elif message.startswith("/help"):
        await event.reply("""
📦 **Команды:**
/mykeys - мои ключи на подарки
/getgift [ключ] - забрать подарок по ключу

🎁 **Как получить подарок:**
Напиши "я с рынка" и отправь подарок
""")
    
    # ===== ЕСЛИ ПРИСЛАЛИ ПОДАРОК =====
    elif "подарок" in message.lower() or "gift" in message.lower():
        await save_gift(event, user_id, message)

async def save_gift(event, user_id, message):
    """Сохраняем полученный подарок"""
    
    # Генерируем уникальный ключ
    gift_key = generate_key()
    gift_id = f"gift_{datetime.now().timestamp()}"
    
    # Сохраняем подарок
    gifts[gift_id] = {
        "name": message,
        "from_user": user_id,
        "key": gift_key,
        "status": "stored",
        "received_at": datetime.now().isoformat()
    }
    
    # Добавляем пользователю
    if user_id not in user_gifts:
        user_gifts[user_id] = []
    user_gifts[user_id].append(gift_id)
    
    # Отправляем ключ
    await event.reply(f"""
✅ **Подарок сохранён!**

🔑 **Ваш уникальный ключ:**
`{gift_key}`

📋 Отправь этот ключ тому, кто хочет забрать подарок.
Он напишет боту: /getgift {gift_key}

/mykeys - посмотреть все ключи
""")

async def show_my_keys(event, user_id):
    """Показать все ключи пользователя"""
    if user_id not in user_gifts or not user_gifts[user_id]:
        await event.reply("📭 У вас нет сохранённых подарков")
        return
    
    text = "🔑 **Ваши ключи:**\n\n"
    for gift_id in user_gifts[user_id]:
        gift = gifts.get(gift_id)
        if gift and gift["status"] == "stored":
            text += f"🎁 {gift['name']}\n"
            text += f"🔑 `{gift['key']}`\n\n"
    
    await event.reply(text)

async def get_gift_by_key(event, message):
    """Забрать подарок по ключу"""
    parts = message.split()
    if len(parts) < 2:
        await event.reply("❌ Введи ключ: /getgift КЛЮЧ")
        return
    
    key = parts[1].strip()
    
    # Ищем подарок по ключу
    found_gift = None
    found_id = None
    for gift_id, gift in gifts.items():
        if gift["key"] == key and gift["status"] == "stored":
            found_gift = gift
            found_id = gift_id
            break
    
    if not found_gift:
        await event.reply("❌ Ключ недействителен или подарок уже забран")
        return
    
    # Отмечаем как выданный
    found_gift["status"] = "claimed"
    found_gift["claimed_at"] = datetime.now().isoformat()
    found_gift["claimed_by"] = (await event.get_sender()).id
    
    # Удаляем из списка пользователя
    if found_gift["from_user"] in user_gifts and found_id in user_gifts[found_gift["from_user"]]:
        user_gifts[found_gift["from_user"]].remove(found_id)
    
    await event.reply(f"""
✅ **Подарок получен!**

🎁 {found_gift['name']}
🔑 Ключ использован

Подарок твой! Храни его или передай дальше.
""")

async def main():
    await client.start()
    me = await client.get_me()
    print(f"🤖 Аккаунт @{me.username} запущен!")
    print("📦 Принимаю подарки и выдаю ключи")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())