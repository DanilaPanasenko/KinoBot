import asyncio
import logging
import requests
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from aiogram.enums import ParseMode
from aiogram import html
from aiogram.types import LinkPreviewOptions, URLInputFile
from bs4 import BeautifulSoup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

logging.basicConfig(level=logging.INFO)
bot = Bot(token="6573804900:AAEHodUK-x9v-VDt26zdN1r-X-I0hCSfMI4")
dp = Dispatcher()

# url = f'https://baskino.im/trillery/'
# response = requests.get(url)
# data = BeautifulSoup(response.text, 'html.parser')

# @dp.message(Command("start"))
# async def hello_start(message: types.Message):
#     builder = ReplyKeyboardBuilder()
#     builder.row(types.KeyboardButton(text='триллеры'))
#     builder.row(types.KeyboardButton(text='ужасы'))
#     await message.answer(text='Выбери категорию', reply_markup=builder.as_markup())
async def start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='триллеры', callback_data='film_trillery'))
    builder.row(types.InlineKeyboardButton(text='комедия', callback_data='film_komedii'))
    await message.answer(text='Выбери категорию', reply_markup=builder.as_markup())

@dp.message(Command("start"))
async def hello_start(message: types.Message):
    await start(message)

@dp.callback_query(F.data == "start_category")
async def category_start(callbacke: types.CallbackQuery):
    await start(callbacke.message)

@dp.callback_query(F.data.startswith('film_'))
async def any_test(callbacke: types.CallbackQuery):
    string_film = callbacke.data.replace('film_', '')
    count = random.randint(1, 10)
    url = f'https://baskino.im/{string_film}/page/{count}/'
    response = requests.get(url)
    data = BeautifulSoup(response.text, 'html.parser')
    list_films = []
    link_film = []
    for film_data in data.find_all('div', class_='shortpost'):
        link = film_data.div.a['href']
        name = film_data.div.a.img['alt']
        films = [name, link]
        list_films.append(films)
        link_film.append(link)
    random_index = random.randint(0, len(list_films) - 1)

    random_link = f'{link_film[random_index]}'

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Смотреть', url=f'{list_films[random_index][1]}'))
    builder.row(types.InlineKeyboardButton(text='Категрии', callback_data='start_category'))
    builder.row(types.InlineKeyboardButton(text='Хочу другой', callback_data=f'film_{string_film}'))


    response_link = requests.get(random_link)
    soup = BeautifulSoup(response_link.text, 'html.parser')
    data_link = soup.find('div', class_='full_movie_desc')
    text_film = data_link.find('div').text

    img_link = soup.find('div', class_='full_movie_info_body')
    url_img = 'https://baskino.im' + img_link.find('img').get('data-src')
    image_from_url = URLInputFile(f'{url_img}')
    await callbacke.message.answer_photo(image_from_url)
    await callbacke.message.answer(f'<b>{list_films[random_index][0]}</b>, \n{text_film}', parse_mode=ParseMode.HTML, reply_markup=builder.as_markup())

@dp.message(F.text == "Круто")
async def wow(message: types.Message):
    await message.reply("Я старался, спасибо!")

@dp.message(F.text == "Обычно")
async def no_wow(message: types.Message):
    await message.reply("Буду работать дальше!")

@dp.message(Command("hello"))
async def hello_name(message: types.Message):
    await message.answer(
        f"Hello, <b>{html.bold(html.quote(message.from_user.full_name))}</b>",
        parse_mode=ParseMode.HTML
    )

# @dp.message(F.text == "список триллеров")
# async def any_test(message: types.Message):
#     for film_data in data.find_all('div', class_='shortpost'):
#         link = film_data.div.a['href']
#         name = film_data.div.a.img['alt']
#         await message.answer(f'{link}, {name}')
# @dp.message(F.text)
# async def any_test(message: types.Message):
    # url = f'https://baskino.im/trillery/'
    # response = requests.get(url)
    # data = BeautifulSoup(response.text, 'html.parser')
    # list_films = []
    # for film_data in data.find_all('div', class_='shortpost'):
    #     link = film_data.div.a['href']
    #     name = film_data.div.a.img['alt']
    #     films = [name, link]
    #     list_films.append(films)
    # random_index = random.randint(0, len(list_films) - 1)
    # await message.answer(f'{list_films[random_index][0]}, {list_films[random_index][1]}')


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
