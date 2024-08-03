import asyncio
import logging
import requests
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from aiogram.enums import ParseMode
from aiogram import html
from aiogram.types import URLInputFile, InputMediaPhoto
from bs4 import BeautifulSoup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

logging.basicConfig(level=logging.INFO)
bot = Bot(token="6573804900:AAEHodUK-x9v-VDt26zdN1r-X-I0hCSfMI4")
dp = Dispatcher()

async def start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='триллеры 🔪', callback_data='film_trillery'))
    builder.row(types.InlineKeyboardButton(text='комедия 🤣', callback_data='film_komedii'))
    builder.row(types.InlineKeyboardButton(text='биография 📖', callback_data='film_biografiya'))
    builder.row(types.InlineKeyboardButton(text='боевики 🔫', callback_data='film_boeviki'))
    builder.row(types.InlineKeyboardButton(text='детективы 🕵️‍♂️', callback_data='film_detektivy'))
    builder.row(types.InlineKeyboardButton(text='драммы 😢', callback_data='film_dramy'))
    builder.row(types.InlineKeyboardButton(text='мелодраммы 💑', callback_data='film_melodrama'))
    builder.row(types.InlineKeyboardButton(text='мультики 👶', callback_data='film_multfilmy-v1'))
    builder.row(types.InlineKeyboardButton(text='приключения 🏔', callback_data='film_priklyucheniya'))
    builder.row(types.InlineKeyboardButton(text='ужасы 🧟‍♂️', callback_data='film_uzhasy'))
    builder.row(types.InlineKeyboardButton(text='фентези 🧛‍♂️', callback_data='film_fentezi'))
    builder.adjust(2)
    await message.answer(text='🎞 Выбери категорию 🎞', reply_markup=builder.as_markup())

@dp.message(Command("start"))
async def hello_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Категрии 🗒', callback_data='start_category'))
    await message.answer(
        f"Привет, <b>{html.bold(html.quote(message.from_user.full_name))}</b>👋. Нажми на кнопку ниже, чтобы выбрать "
        f"вашу любимую категорию и бот пришлет вам подходящий фильм 🎥. ",
        parse_mode=ParseMode.HTML, reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data == "start_category")
async def category_start(callbacke: types.CallbackQuery):
    await start(callbacke.message)

@dp.callback_query(F.data.startswith('film_'))
async def any_test(callbacke: types.CallbackQuery):
    string_film = callbacke.data.replace('film_', '')
    url = f'https://baskino.im/{string_film}/'
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
    builder.row(types.InlineKeyboardButton(text='Смотреть 🔍', url=f'{list_films[random_index][1]}'))
    builder.row(types.InlineKeyboardButton(text='Хочу другой 😐', callback_data=f'film_{string_film}'))
    builder.row(types.InlineKeyboardButton(text='Изменить категорию 🔄', callback_data='start_category'))
    response_link = requests.get(random_link)
    soup = BeautifulSoup(response_link.text, 'html.parser')
    data_link = soup.find('div', class_='full_movie_desc')
    text_film = data_link.find('div').text
    img_link = soup.find('div', class_='full_movie_info_body')
    url_img = 'https://baskino.im' + img_link.find('img').get('data-src')
    image_from_url = URLInputFile(f'{url_img}')
    await callbacke.message.answer_photo(image_from_url)
    await callbacke.message.answer(
        f'<b>{list_films[random_index][0]}</b> \n{text_film}',
        parse_mode=ParseMode.HTML,
        reply_markup=builder.as_markup())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())