import requests
from bs4 import BeautifulSoup
import random

dict_category = {'триллеры': 'trillery'}
category = input()
category_input = dict_category.get(category)

count = random.randint(1, 10)

url = f'https://baskino.im/{category_input}/page/{count}/'
response = requests.get(url)
data = BeautifulSoup(response.text, 'html.parser')

list_films = []
link_film = []
img_film = []
for film_data in data.find_all('div', class_='shortpost'):
    link = film_data.div.a['href']
    name = film_data.div.a.img['alt']
    films = [name, link]
    list_films.append(films)
    link_film.append(link)

random_index = random.randint(0, len(list_films) - 1)
random_link = f'{link_film[random_index]}'
random_film = f'{list_films[random_index][0]}, {list_films[random_index][1]}'

response_link = requests.get(random_link)
soup = BeautifulSoup(response_link.text, 'html.parser')
data_link = soup.find('div', class_='full_movie_desc')
img_link = soup.find('div', class_='full_movie_info_body')
text_film = data_link.find('div').text
url_img = 'https://baskino.im' + img_link.find('img').get('data-src')

print(count)
print(text_film)
print(random_film)

print(url_img)

