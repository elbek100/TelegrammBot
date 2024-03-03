import datetime
import os
import asyncio

import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Router, Bot, Dispatcher
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from database import create_table, info
from aiocron import crontab

dp = Dispatcher()
load_dotenv()
scheduler = AsyncIOScheduler()
token = os.getenv('BOT_TOKEN')
bot = Bot(token)


@dp.message(CommandStart())
async def start(message: Message):
    info = KeyboardButton(text='info')
    markup = ReplyKeyboardMarkup(keyboard=[[info]], resize_keyboard=True)
    await message.answer(f"Assalomu aleykum {message.from_user.first_name}\nXodimlarning tug'ilgan kunini eslatib turishim uchun 'info' tugmasini bosing", reply_markup=markup)


@dp.message(lambda msg: msg.text == 'info')
async def info_birth_date(message: Message):
    await message.answer("Sorovingiz uchun rahmat \nXodimlarning tug'ilgan kunini kutyabman", reply_markup=ReplyKeyboardRemove())

    async def send_user_info():
        data = info()
        if data:
            for record in data:
                id, first_name, last_name, img, birth_date, role_id = record
                await message.answer(f"Bugun {first_name} {last_name}ning tug'ilgan kuni, tabriklaymiz! 🎉🎂")
                await message.answer(f"{birth_date}")
                if os.path.exists(img):
                    URL = 'https://api.telegram.org/bot' + os.getenv('BOT_TOKEN') + '/sendDocument'

                    with open(img, 'rb') as file:
                        files = {'document': (img, file)}
                        payload = {'chat_id': message.chat.id}
                        requests.post(URL, data=payload, files=files)
    scheduler.add_job(send_user_info,'cron', hour=8, minute=0)
    scheduler.start()
    while True:
        await asyncio.sleep(1)


async def main():
    create_table()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
