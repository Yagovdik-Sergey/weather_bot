import asyncio
import requests
import datetime
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Напишите название города, и я пришлю сводку погоды!')

@dp.message()
async def get_weather(message: Message):

    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }

    try:
        r = requests.get(
            f"http://ru.api.openweathermap.org/data/2.5/weather?q={message.text}&appid={os.getenv('WEATHER_TOKEN')}&units=metric"
        )
        data = r.json()

        city = data['name']
        cur_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wb = code_to_smile[weather_description]
        else:
            wb = 'Посмотри в окно, неизвестная погода'

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = sunset_timestamp - sunrise_timestamp

        await message.answer(f'''***{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}***
    Погода в городе {city}
    {wb}
    Температура: {cur_weather} °C
    Влажность: {humidity} %
    Давление: {int(int(pressure) * 0.75)} мм. рт. столба
    Ветер: {wind} м/с
    Восход солнца: {sunrise_timestamp}
    Закат: {sunset_timestamp}
    Продолжительность светового дня: {length_of_the_day}
    ***Хорошего дня!***
    ''')

    except:
        await message.answer('\U00002620 Проверьте название города \U00002620')

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())