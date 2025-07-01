from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import db

API_TOKEN = '7795364666:AAEyFR8p4ddUKl402Wro_qrfw4Vlmgvul2s'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
db.init_db()

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Отправить номер ☎️', request_contact=True)
    )
    await message.answer("Привет! Нажми кнопку ниже, чтобы подтвердить свой номер телефона и получать уведомления:", reply_markup=kb)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def contact_handler(message: types.Message):
    phone = message.contact.phone_number
    if not phone.startswith('+'):
        phone = '+' + phone
    db.save_user(phone, message.chat.id)
    await message.answer(f"Спасибо! Теперь ты будешь получать уведомления для номера: {phone}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
