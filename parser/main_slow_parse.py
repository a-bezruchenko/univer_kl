# coding: utf8
# этот файл — один из исполняемых
# скрипт проходит по тем страницам, которые были записаны в базу данных, но не имеют текста

import asyncio
from aiohttp import ClientSession, ClientResponseError

from safe_get import fetch_html
from parser_funcs import parse_html, scrap_post_page
import db_init
import db_parser

async def download_and_parse(urls, session, queue):
    for url in urls:
        try:
            html_text = await fetch_html("https://v1.ru"+url, session)
        except ClientResponseError:
            print("Ошибка при обращении к " + url)
            continue
        html = parse_html(html_text)
        result = scrap_post_page(html)
        result['link'] = url
        await queue.put((result, url))
    await queue.put(True)

async def load_parsed_data_to_db(queue, db_con):
    while True:
        q_data = await queue.get()
        if q_data == True:
            break
        data, num = q_data
        await asyncio.gather(db_parser.add_values(data, db_con))
        print(f"Страница {num} обработана")
        queue.task_done()

async def slow_parse_site():
    db_con = await db_init.init()
    async with ClientSession() as session:
        pages_list = list(map(lambda x: x[0], await db_parser.get_incomplete_records(db_con)))
        queue = asyncio.Queue()
        producer = asyncio.create_task(download_and_parse(pages_list, session, queue))
        consumer = asyncio.create_task(load_parsed_data_to_db(queue, db_con))
        await asyncio.gather(producer, consumer)
        #await queue.join()

if __name__ == "__main__":
    asyncio.run(slow_parse_site())