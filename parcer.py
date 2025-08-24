import json
import requests
from datetime import datetime

now_year = datetime.now().year
year = input(f'Введите год (по умолчанию - {now_year}): ')
if year:
    while True:
        try:
            year = int(year)
            break
        except ValueError:
            year = input('Введите год числом: ')
else:
    year = datetime.now().year
responce = requests.get(f'https://www.consultant.ru/law/ref/calendar/proizvodstvennye/{year}/')

while responce.status_code != 200:
    year = input('Страница не найдена, введите правильный год: ')
    responce = requests.get(f'https://www.consultant.ru/law/ref/calendar/proizvodstvennye/{year}/')
if year == 2024 or year == 2020:
    responce = requests.get(f'https://www.consultant.ru/law/ref/calendar/proizvodstvennye/{year}b/')

holidays = {month: [] for month in range(12)}
preholidays = {month: [] for month in range(12)}

info = tuple(map(str.strip, responce.text.split('\n')))
filtered_info = list()
for line in info:
    if (line.find('weekend') != -1 or line.find('preholiday') != -1) and any(c.isdigit() for c in line):
        filtered_info.append(line)
for line in range(len(filtered_info)):
    for elem in filtered_info[line].split('class="'):
        if elem.startswith('weekend') or elem.startswith('holiday weekend'):
            date = int(''.join(filter(str.isdigit, elem)))
            holidays[line].append(date)
        elif elem.startswith('preholiday'):
            date = int(''.join(filter(str.isdigit, elem)))
            preholidays[line].append(date)

result = {'holidays': [], 'preholidays': []}

for month, dates in holidays.items():
    if dates:
        for d in dates:
            date = datetime(int(year), month + 1, d)
            result['holidays'].append(date.strftime("%Y-%m-%d"))

for month, dates in preholidays.items():
    if dates:
        for d in dates:
            date = datetime(int(year), month  + 1, d)
            result['preholidays'].append(date.strftime("%Y-%m-%d"))

with open(f'result_{year}.json', 'w') as file:
    json.dump(result, file, indent=2)
    print(f'Данные сохранены в result_{year}.json')
