import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

TOKEN = "7625252064:AAHTu2HlifuD0DqAsW1dn4NfhFwaMFpqeHY"
ADMIN_ID = "@sava_il"
CHANNEL_ID = "@tradelovers101"  

logging.basicConfig(level=logging.INFO)

from aiogram.client.default import DefaultBotProperties

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Добро пожаловать, меня зовут Сава и я эксперт по трейдингу. Оставь заявку на вступление, пиши- хочу в канал, принимаю 24/7:")

@dp.message()
async def receive_application(message: types.Message):
    user = message.from_user
    text = f"Заявка от @{user.username} (ID: {user.id}):\n{message.text}"
    
    approve_button = InlineKeyboardButton("✅ Заебись", callback_data=f"approve_{user.id}")
    reject_button = InlineKeyboardButton("❌ Хуета", callback_data=f"reject_{user.id}")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[approve_button, reject_button]])
    
    await bot.send_message(ADMIN_ID, text, reply_markup=keyboard)
    await message.answer("Ваша заявка отправлена администратору.")

@dp.callback_query()
async def process_callback(callback_query: types.CallbackQuery):
    action, user_id = callback_query.data.split("_")
    user_id = int(user_id)
    
    if action == "approve":
        invite_link = await bot.create_chat_invite_link(CHANNEL_ID, member_limit=1)
        await bot.send_message(user_id, f"Ваша заявка одобрена! Вот ссылка на канал: {invite_link.invite_link}")
        await callback_query.message.edit_text("Заявка одобрена ✅")
    elif action == "reject":
        await bot.send_message(user_id, "Ваша заявка отклонена.")
        await callback_query.message.edit_text("Заявка отклонена ❌")
    
    await callback_query.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

