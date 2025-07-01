from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import asyncio
import os
import db

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN, session=AiohttpSession())
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

@router.message(lambda msg: msg.text == "/start")
async def start(message: Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton(text="Отправить номер ☎️", request_contact=True)
    )
    await message.answer("Привет! Нажми кнопку ниже, чтобы отправить номер:", reply_markup=kb)

@router.message(lambda msg: msg.contact is not None)
async def save_contact(message: Message):
    phone = message.contact.phone_number
    if not phone.startswith('+'):
        phone = '+' + phone
    db.save_user(phone, message.chat.id)
    await message.answer(f"Спасибо! Ты зарегистрирован по номеру {phone}.")

async def main():
    db.init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
