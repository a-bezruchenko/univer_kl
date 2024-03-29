# coding: utf8
# этот файл — один из исполняемых
# скрипт быстро пробегается по главной странице, собирая доступную информацию,
# но не заходит на страницы и не собирает текст
import sys
import asyncio
from aiohttp import ClientSession, ClientResponseError

from safe_get import fetch_html
from parser_funcs import parse_html, scrap_news_page, get_pages_count
import db_init
import db_parser
from util import getLastFrom

def get_prev_pages(pages_count, last_page_to_check=-1):
    if last_page_to_check == -1:
        last_page_to_check = pages_count
    return 

async def download_and_parse(urls, session, queue):
    for url in urls:
        try:
            html_text = await fetch_html(url, session)
        except ClientResponseError:
            print("Ошибка при обращении к " + url)
            continue
        html = parse_html(html_text)
        result = scrap_news_page(html)
        num = getLastFrom(url, "=")
        await queue.put((result, num))
    await queue.put(True)

async def load_parsed_data_to_db(queue, db_con):
    while True:
        q_data = await queue.get()
        if q_data == True:
            break
        data_list, num = q_data
        await asyncio.gather(*[db_parser.add_values(el, db_con) for el in data_list])
        print(f"Страница {num} обработана")
        queue.task_done()

async def quick_parse_site(first_page_to_check, last_page_to_check):
    db_con = await db_init.init()
    async with ClientSession() as session:
        pages_list = [f"https://v1.ru/text/?page={x}" for x in range(first_page_to_check, last_page_to_check+1)]
        queue = asyncio.Queue()
        producer = asyncio.create_task(download_and_parse(pages_list, session, queue)) 
        consumer = asyncio.create_task(load_parsed_data_to_db(queue, db_con))
        await asyncio.gather(producer, consumer)

if __name__ == "__main__":
    ERROR = False
    if (len(sys.argv)==1):
        print("Не удалось запустить парсер: необходимо указать количество страниц")
        ERROR = True
    elif (len(sys.argv)==2):
        first_page_to_check = 1
        last_page_to_check = int(sys.argv[1])
    else:
        first_page_to_check = int(sys.argv[1])
        last_page_to_check = int(sys.argv[2])
    
    if first_page_to_check < 1:
        print("Неправильно указана первая страница")
        ERROR = True

    if not ERROR:
        if first_page_to_check > last_page_to_check:
            first_page_to_check, last_page_to_check = last_page_to_check, first_page_to_check
        print(f"Проверяем страницы с {first_page_to_check} по {last_page_to_check}")
        asyncio.run(quick_parse_site(first_page_to_check, last_page_to_check))