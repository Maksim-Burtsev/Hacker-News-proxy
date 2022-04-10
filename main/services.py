import re
import string
from typing import Union

import html2text
import requests
import fake_useragent


def add_query_params_to_link(url: str, request_items: dict) -> str:
    """
    Добавляет к ссылке query-параметры из словаря
    """
    url += '?'
    k = 0
    for key, values in request_items:
        if k == 0:
            url += f'{key}={values[0]}'
        else:
            url += f'&{key}={values[0]}'
        k += 1

    return url


def _parser(url: str) -> Union[str, None]:
    """
    Парсит html-страницу и подключает к ней стили
    """

    user = fake_useragent.UserAgent().random
    headers = {
        'user-agent': user,
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_text_list = response.text.split('<head>')

        connect_css = """<head><link rel="stylesheet" href={% static 'main/style.css'%}/>"""

        html_text_list.insert(1, connect_css)

        return ''.join(html_text_list)


def _replace_and_create_file(html_text: str, filename: str) -> None:
    """
    Добавляет ко всем словам html-страницы с длиной равной шести ™, обновляет ссылки и записывает все в файл 
    """

    text = _clean_text_from_html(html_text)

    six_lenght_words = list(
        set([word for word in text.split() if len(word) == 6]))

    for i in range(len(six_lenght_words)):
        html_text = html_text.replace(
            six_lenght_words[i], f'{six_lenght_words[i]}™')

    text = _clean_extra_tm(html_text)

    res = _update_links_and_static(text)

    with open(f'main\\templates\\main\\{filename}.html', 'w', encoding='utf-8') as f:
        f.write(res)


def _clean_text_from_html(html_text: str) -> str:
    """
    Очищает страницу от html-тегов и служебных символов
    """

    h = html2text.HTML2Text()
    h.ignore_links = True

    text = h.handle(html_text)
    for char in string.punctuation:
        text = text.replace(char, ' ')

    return text


def _clean_extra_tm(html_text: str) -> str:
    """
    Удаляет все лишние ™, которые попали в процессе обработки

    Hacker™s -> Hackers
    remote™s -> remote
    """
    text = ''
    for i in range(len(html_text)-1):
        if html_text[i] == '™' and html_text[i+1].isalpha():
            text += ''
        else:
            text += html_text[i]

    text += html_text[-1]

    regex = re.compile(r'<a href="(.*)™+?">')

    for a in regex.findall(text):
        text = text.replace(f'<a href="{a}™"', f'<a href="{a}"')

    return text


def _update_links_and_static(text: str) -> str:
    """
    Убирает со страницы все ссылки, которые ведут на HackerNews и подключает статические файлы
    """

    text = '{% load static %}' + text

    text = text.replace('https://news.ycombinator.com', '')

    for i in ('favicon.ico', 'y18.gif'):
        text = text.replace(i, "{% static 'main/logo.ico' %}")

    return text


def get_updated_html_file(link: str, filename: str) -> None:
    """
    Парсит html-страницу и добавляет ™ к каждому слову с длиной равной шести. Готовая страница записывается в файл .html
    """

    html_text = _parser(link)
    _replace_and_create_file(html_text, filename)