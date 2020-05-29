# encode: utf-8
# этот файл — основной исполняемый файл парсера
import re
import datetime
from time import sleep
import sys
import requests
import os.path

import asyncio
from aiohttp import ClientSession

from bs4 import BeautifulSoup as BS

from safe_get import fetch_html
from reactor_parse import scrapPage, getPrevPages, parse_html
from util import getName, cutLastFrom, append_to_file
import requests

LAST_PAGE_CHECKED = ""

def getPrevPages(pages_count, last_page_checked = 1):
    return [f"https://v1.ru/text/?page={x}" for x in range(last_page_checked, pages_count+1)] 


async def quick_parse_site():
    async with ClientSession() as session:
        html = await download_parsed_page(LAST_PAGE_CHECKED, session)
        
        pages = getPrevPages()


    #"https://v1.ru/text/?page=1"


# async def bulk_save_source_image_by_tag(url):
#     # считать прогресс
#     # в файле записана последняя проверенная страница
    
    
#     progress_file_name = "output/lastpage.txt"

#     if not os.path.exists("output"):
#         os.mkdir("output")

#     if os.path.isfile(progress_file_name):  # если файла нет, то и прогресс не надо считывать
#         print("найден файл прогресса")
#         with open(progress_file_name, "r") as f:
#             LAST_PAGE_CHECKED = f.read()
#     else:
#         print("файл прогресса не найден")

#     if LAST_PAGE_CHECKED == "":
#         LAST_PAGE_CHECKED = url
#         print("файл прогресса пуст")
#     else:
#         print("продолжаем с ", LAST_PAGE_CHECKED)

#     # продолжить
#     async with ClientSession() as session:
#         html = await download_parsed_page(LAST_PAGE_CHECKED, session)
#         tag_pages_list = getPrevPages(url, html)
#         queue = asyncio.Queue()
#         producers = [asyncio.create_task(download_and_parse(page, session, queue)) for page in tag_pages_list]
#         file_loader = asyncio.create_task(load_parsed_data_to_db(queue))
#         await asyncio.gather(*producers)
#         await queue.join()
#         file_loader.cancel()
#         await asyncio.gather(file_loader, return_exceptions=True)

# async def load_parsed_data_to_file(queue):
#     global LAST_PAGE_CHECKED
#     while True:
#          = await queue.get()
#         print(str.format("Начата обработка страницы {0}", page))
#         LAST_PAGE_CHECKED = page
#         # следующий кусок кода независимый друг от друга и мы можем выполнить их паралельно

#         print(str.format("Страница {0} обработана", page))
#         queue.task_done()

# async def download_and_parse(page, session, queue):
#     html_text = await fetch_html(page, session)
#     html = parse_html(html_text)
#     result = scrapPage(html)
#     await queue.put(result)

if __name__ == "__main__":
    asyncio.run(quick_parse_site())

    