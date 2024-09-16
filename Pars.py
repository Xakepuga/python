from bs4 import BeautifulSoup
import pandas as pd

# Укажите путь к вашему локальному HTML-файлу
file_path = '123.html'  # Путь к вашему файлу в папке проекта

# Укажите путь для файла Excel
excel_path = 'output.xlsx'

# Функция для получения данных из локального HTML-файла
def get_data_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Найдите таблицу на странице
    table = soup.find('table')  # Убедитесь, что это правильный селектор для вашей таблицы
    if not table:
        print('Таблица не найдена в HTML-файле.')
        return [], []

    # Получение заголовков таблицы
    headers = []
    header_row = table.find('tr')  # Предполагаем, что заголовки находятся в первой строке
    if header_row:
        headers = [th.text.strip() for th in header_row.find_all('th')]
    if not headers:
        print('Заголовки не найдены в таблице.')

    # Получение данных таблицы
    rows = table.find_all('tr')[1:]  # Пропускаем первую строку (заголовки)
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)  # Сохраняем все значения в строке

    return headers, data

# Получаем данные из HTML-файла
headers, data = get_data_from_html(file_path)

# Проверка, есть ли данные для записи
if not data:
    print('Нет данных для записи в файл.')
else:
    # Определите количество столбцов в самой большой строке
    num_columns = max(len(row) for row in data) if data else len(headers)
    columns = headers if headers else [f'Колонка{i+1}' for i in range(num_columns)]

    # Убедитесь, что все строки имеют одинаковое количество столбцов, добавьте пустые строки, если нужно
    data = [row + [''] * (num_columns - len(row)) for row in data]

    # Создайте DataFrame
    df = pd.DataFrame(data, columns=columns)

    # Перезаписать существующий файл или создать новый
    df.to_excel(excel_path, index=False)

    print('Парсинг завершен. Данные сохранены в', excel_path)