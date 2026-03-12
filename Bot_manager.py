1import asyncio
from telethon import TelegramClient, events
from telethon.tl.custom import Button
import os
import logging
from datetime import datetime

# ========== НАСТРОЙКИ ==========
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== КОНФИГУРАЦИЯ ==========
BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_ID = int(os.environ.get('API_ID', 35494524))
API_HASH = os.environ.get('API_HASH', '0e465149f428a082cc47a7c7d016c179')
ACCESS_CODE = "8532"
AUTHORIZED_USERS = []

# ========== СОСТОЯНИЕ ==========
waiting_for_code = {}

# ========== СОЗДАНИЕ БОТА ==========
bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_id = event.sender_id
    if user_id in AUTHORIZED_USERS:
        await show_main_menu(event)
    else:
        await event.reply("🔐 **Введите код доступа:**")
        waiting_for_code[user_id] = True

@bot.on(events.NewMessage)
async def handler(event):
    user_id = event.sender_id
    text = event.message.message.strip()
    
    if user_id in waiting_for_code:
        if text == ACCESS_CODE:
            AUTHORIZED_USERS.append(user_id)
            del waiting_for_code[user_id]
            await event.reply("✅ **Код верный!**")
            await show_main_menu(event)
        else:
            await event.reply("❌ Неверный код. Попробуйте снова:")
        return
    
    if user_id in AUTHORIZED_USERS:
        if "я с рынка" in text.lower():
            await event.reply("Отправляй подарок! 🎁")
        elif text == "1" or "авторизация" in text.lower():
            await auth_menu(event)
        elif text == "2" or "удалённые" in text.lower():
            await event.reply("🗑 Функция в разработке")
        elif text == "3" or "автоответ" in text.lower():
            await event.reply("🤖 Автоответ активен:\n'я с рынка' → 'Отправляй подарок'")

async def show_main_menu(event):
    menu = """
📱 **МЕНЕДЖЕР АККАУНТА**

1️⃣ Авторизация номера
2️⃣ Удалённые сообщения
3️⃣ Автоответы
4️⃣ Сессии
5️⃣ Настройки

**Код доступа:** 8532
"""
    await event.reply(menu, buttons=[
        [Button.text("📱 Авторизация", resize=True)],
        [Button.text("🗑 Удалённые")],
        [Button.text("🤖 Автоответ")],
    ])

async def auth_menu(event):
    await event.reply("📱 **Отправьте ваш контакт:**", buttons=[
        [Button.request_contact("📱 Поделиться контактом")]
    ])

@bot.on(events.NewMessage(func=lambda e: e.message.contact))
async def handle_contact(event):
    contact = event.message.contact
    await event.reply(f"✅ Контакт получен!\n📱 Номер: {contact.phone_number}")

async def main():
    me = await bot.get_me()
    logger.info(f"✅ Бот @{me.username} запущен! Код: 8532")
    await bot.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
