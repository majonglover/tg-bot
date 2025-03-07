import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties

TOKEN = "7625252064:AAHTu2HlifuD0DqAsW1dn4NfhFwaMFpqeHY"
ADMIN_ID = "2125587179"  # Замените на числовой ID администратора
CHANNEL_ID = "@tradelovers101"  

logging.basicConfig(level=logging.INFO)

# Используем DefaultBotProperties для задания parse_mode
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(bot)  # Передаем bot в Dispatcher

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Добро пожаловать, меня зовут Сава и я эксперт по трейдингу. Оставь заявку на вступление, пиши- хочу в канал, принимаю 24/7:")

@dp.message()
async def receive_application(message: types.Message):
    user = message.from_user
    text = f"Заявка от @{user.username} (ID: {user.id}):\n{message.text}"
    
    # Применяем правильный синтаксис для InlineKeyboardButton
    approve_button = InlineKeyboardButton(text="✅ Заебись", callback_data=f"approve_{user.id}")
    reject_button = InlineKeyboardButton(text="❌ Хуета", callback_data=f"reject_{user.id}")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[approve_button, reject_button]])
    
    await bot.send_message(ADMIN_ID, text, reply_markup=keyboard)
    await message.answer("Ваша заявка отправлена администратору.")

@dp.callback_query()
async def process_callback(callback_query: types.CallbackQuery):
    action, user_id = callback_query.data.split("_")
    user_id = int(user_id)
    
    if action == "approve":
        # Создаем инвайт-ссылку для канала
        invite_link = await bot.export_chat_invite_link(CHANNEL_ID)
        await bot.send_message(user_id, f"Ваша заявка одобрена! Вот ссылка на канал: {invite_link}")
        await callback_query.message.edit_text("Заявка одобрена ✅")
    elif action == "reject":
        await bot.send_message(user_id, "Ваша заявка отклонена.")
        await callback_query.message.edit_text("Заявка отклонена ❌")
    
    await callback_query.answer()

async def main():
    # Начинаем polling
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())  # Вызываем main через asyncio


