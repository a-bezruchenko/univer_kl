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

async def download_and_parse(url, session, queue):
    html_text = await fetch_html(url, session)
    html = parse_html(html_text)
    result = scrap_news_page(html)
    num = getLastFrom(url, "=")
    await queue.put((result, num))

async def quick_parse_site():
    async with ClientSession() as session:
        parsed_content = parse_html(await fetch_html("https://v1.ru/text/", session))
        pages_count = get_pages_count(parsed_content)
        pages_list = getPrevPages(pages_count)
        db_con = await db.init()
        queue = asyncio.Queue()
        producers = [asyncio.create_task(download_and_parse(page, session, queue)) for page in pages_list]
        consumer = asyncio.create_task(load_parsed_data_to_db(queue, db_con))
        await asyncio.gather(*producers)
        await queue.join()
        consumer.cancel()
        await asyncio.gather(consumer, return_exceptions=True)

async def load_parsed_data_to_db(queue, db_con):
    while True:
        data_list, num = await queue.get()
        await asyncio.gather(*[db.add_values(el, db_con) for el in data_list])
        print(f"Страница {num} обработана")
        queue.task_done()

if __name__ == "__main__":
    asyncio.run(quick_parse_site())