# coding: utf8
# этот файл — один из исполняемых
# скрипт быстро пробегается по главной странице, собирая доступную информацию,
# но не заходит на страницы и не собирает текст
import asyncio
from aiohttp import ClientSession

from safe_get import fetch_html
from parser_funcs import parse_html, scrap_news_page, get_pages_count
import db
from util import getLastFrom

def getPrevPages(pages_count, last_page_checked = 1):
    return [f"https://v1.ru/text/?page={x}" for x in range(last_page_checked, pages_count+1)]

async def download_and_parse(urls, session, queue):
    for url in urls:
        html_text = await fetch_html(url, session)
        html = parse_html(html_text)
        result = scrap_news_page(html)
        num = getLastFrom(url, "=")
        await queue.put((result, num))

async def quick_parse_site():
    db_con = await db.init()
    async with ClientSession() as session:
        parsed_content = parse_html(await fetch_html("https://v1.ru/text/", session))
        pages_count = get_pages_count(parsed_content)
        pages_list = getPrevPages(pages_count)
        queue = asyncio.Queue()
        producer = asyncio.create_task(download_and_parse(pages_list, session, queue)) 
        consumer = asyncio.create_task(load_parsed_data_to_db(queue, db_con))
        await asyncio.gather(producer, consumer)
        await queue.join()

async def load_parsed_data_to_db(queue, db_con):
    while True:
        data_list, num = await queue.get()
        await asyncio.gather(*[db.add_values(el, db_con) for el in data_list])
        print(f"Страница {num} обработана")
        queue.task_done()

if __name__ == "__main__":
    asyncio.run(quick_parse_site())