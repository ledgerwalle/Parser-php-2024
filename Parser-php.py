
import os
import requests

def download_file(url, destination):
    try:
        response = requests.get(url, allow_redirects=False)

        if response.status_code == 200:
            with open(destination, 'wb') as file:
                file.write(response.content)
            print(f"Файл успешно загружен в {destination}")

            # Проверка существования файла
            if os.path.isfile(destination):
                print("Файл существует. Выполняем вторую часть кода.")
                # Ваш код для второй части здесь
            else:
                print("Файл не существует после загрузки.")
        elif response.status_code == 302 and 'Location' in response.headers:
            # Обработка перенаправления
            redirect_url = response.headers['Location']
            print(f"Обнаружено перенаправление. Новый URL: {redirect_url}")
            download_file(redirect_url, destination)
        else:
            print(f"Не удалось скачать файл {url}. Статус код: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")

if __name__ == "__main__":
    # Замените URL и destination на соответствующие значения
    url = "https://example.com/"
    destination = "index.html"

    download_file(url, destination)
################################## Код сверху найтет сайт и созддасть index.html со всеми директориями ##############################################

import urllib.request
from urllib.parse import urlparse, urlunparse

def encode_url(url):
    # Разбиваем URL на компоненты
    parsed_url = urlparse(url)

    # Преобразуем доменное имя в Punycode
    encoded_netloc = parsed_url.netloc.encode('idna').decode('utf-8')

    # Собираем измененный URL
    encoded_url = urlunparse((parsed_url.scheme, encoded_netloc, parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment))

    return encoded_url

url_with_cyrillic = "https://example.com/"
encoded_url = encode_url(url_with_cyrillic)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# Кодируем URL
req = urllib.request.Request(encoded_url, headers=headers)
response = urllib.request.urlopen(req)

# Получение содержимого документа
php_code = response.read().decode('utf-8')

# Имя файла для сохранения копии кода PHP
file_name = "php_code.txt"

# Запись кода PHP в текстовый файл
with open(file_name, 'w', encoding='utf-8') as f:
    # Перебор символов и специальных символов
    for char in php_code:
        # Экранирование специальных символов
        if char in ['"', "'", "\\"]:
            char = "\\" + char
        f.write(char)

print("Копия кода PHP сохранена в файле: " + file_name)


##################################### Код выше проверит папку где запущен скрипт на наличие index.html или других .html #############################################################
import time
# Добавляем таймслип (паузу) в 5 секунд (можно изменить по необходимости)
time.sleep(5)

##############################код выше даст ожидание 5 сикунд  #################################
import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Папка для сохранения скачанных файлов
download_folder = "downloaded_files"
# Список базовых URL
base_urls = ["https://example.com/"]

# Выбираем первый адрес в качестве базового URL
base_url = base_urls[0]
# Проверить, существует ли папка downloaded_files, и создать, если не существует
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Функция для преобразования относительного URL в абсолютный
def absolute_url(base_url, relative_url):
    if not base_url or not base_url.startswith(('http://', 'https://')):
        raise ValueError(f"Базовый URL '{base_url}' не является полным URL-адресом. Пропускается.")

    # Если относительный URL не начинается с '/', считаем, что он относительный
    if not relative_url.startswith('/'):
        # Используем текущую директорию файла HTML как базовый URL
        base_url = os.path.dirname(base_url)

    return urljoin(base_url, relative_url)

# Функция для преобразования URL в имя файла
def url_to_filename(url):
    # Извлекаем имя файла из URL
    filename = os.path.basename(urlparse(url).path)
    # Заменяем недопустимые символы в имени файла
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return filename

# Функция для скачивания файла по URL
def download_file(url):
    try:
        if not url.startswith(("http", "https")):
            print(f"URL '{url}' не является полным URL-адресом. Пропускается.")
            return

        response = requests.get(url)
        response.raise_for_status()  # Бросает исключение в случае ошибки HTTP

        filename = os.path.join(download_folder, urlparse(url).path.lstrip('/'))

        # Проверяем, существует ли папка для файла, и создаем, если не существует
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Проверяем, существует ли файл filename, и создаем, если не существует
        if not os.path.exists(filename):
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"Файл {filename} успешно скачан.")
        else:
            print(f"Файл {filename} уже существует. Пропускается.")
    except requests.exceptions.RequestException as e:
        print(f"Не удалось скачать файл {url}. Ошибка: {e}")

# Получаем список всех файлов HTML в текущей директории
html_files = [file for file in os.listdir() if file.endswith(".html")]

for html_file_path in html_files:
    # Открываем файл и считываем его содержимое
    with open(html_file_path, "r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, "html.parser")

        # Ищем тег <base> с атрибутом href
        base_tag = soup.find("base", href=True)

        # Если тег <base> найден, используем его значение как базовый URL
        base_url = base_tag["href"] if base_tag else base_url

        # Ищем все теги <script> с атрибутом src
        script_tags = soup.find_all("script", src=True)

        # Извлекаем значения атрибута src
        script_urls = [absolute_url(base_url, tag["src"]) for tag in script_tags if "src" in tag.attrs]

        # Ищем все теги <link> с атрибутом href
        link_tags = soup.find_all("link", href=True)

        # Извлекаем значения атрибута href
        link_urls = [absolute_url(base_url, tag["href"]) for tag in link_tags if "href" in tag.attrs]

        # Ищем все теги <a> с атрибутом href
        a_tags = soup.find_all("a", href=True)

        # Извлекаем значения атрибута href
        a_urls = [absolute_url(base_url, tag["href"]) for tag in a_tags if "href" in tag.attrs]

        # Ищем все теги <img> с атрибутом src
        img_tags = soup.find_all("img", src=True)

        # Извлекаем значения атрибута src
        img_urls = [absolute_url(base_url, tag["src"]) for tag in img_tags if "src" in tag.attrs]

        # Ищем все теги <source> с атрибутом src
        source_tags = soup.find_all("source", src=True)

        # Извлекаем значения атрибута src
        source_urls = [absolute_url(base_url, tag["src"]) for tag in source_tags if "src" in tag.attrs]

        # Ищем теги <div> с атрибутом style
        div_tags = soup.find_all("div", style=True)

        # Извлекаем значения атрибута style
        for tag in div_tags:
            # Используем регулярное выражение для поиска URL в значении атрибута style
            style_value = tag["style"]
            match = re.search(r"url\('([^']+)'\)", style_value)
            if match:
                url = match.group(1)
                full_url = absolute_url(base_url, url)
                img_urls.append(full_url)  # Добавляем URL в общий список

        # Объединяем списки URL-адресов
        all_urls = script_urls + link_urls + a_urls + img_urls + source_urls
        print("Начало скачивания файлов отсюда ")

        # Скачивание и сохранение файлов
        for url in all_urls:
            download_file(url)
        # Вывод уведомления
        print("Все файлы успешно скачаны.")
############################## Код выше выкачает все что сможет вмесьте с доступными php если указать на его путь ###################################
