import os

from random import choice
import requests
import asyncio
from loguru import logger
from dotenv import load_dotenv, find_dotenv
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message


load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")
dp = Dispatcher()


@dp.message(Command("start"))
async def command_start_handler(message: Message):
    await message.answer("Привет! Я эхо-бот!")


# @dp.message()
# async def echo(message: Message):
#     await message.answer(message.text)

@dp.message(Command("anekdot"))
async def send_anekdot(message: Message):
    response = requests.get('http://www.anekdot.ru/random/anekdot/')
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        jokes = soup.find_all('div', class_='text')

        random_joke = choice(jokes).text.strip()
        anekdot = random_joke
    else:
        anekdot = "Не удалось получить анекдот"

    await message.answer(anekdot)


async def main():
    logger.add('file.log',
               format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
               rotation="3 days")

    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())