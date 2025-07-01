from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ContentType
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.client.session.aiohttp import AiohttpSession
import asyncio
import db
import os

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

@router.message(content_types=ContentType.CONTACT)
async def save_contact(message: Message):
    phone = message.contact.phone_number
    if not phone.startswith('+'):
        phone = '+' + phone
    db.save_user(phone, message.chat.id)
    await message.answer(f"Спасибо! Вы зарегистрированы по номеру {phone}")

async def main():
    db.init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
