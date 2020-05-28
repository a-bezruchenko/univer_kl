from time import time as current_time
import os.path
import signal
from signal import SIGINT, SIGTERM

import asyncio
from aiohttp import ClientSession

from util import getName, cutLastFrom, append_to_file
from reactor_parse import scrapPage, getPrevPages, parse_html


LAST_PAGE_CHECKED = ""
# download - качает указанные картинки
# save_source - сохраняет ссылки на указанные картинки
# bulk - при прерывании по Ctrl+C сохраняет наработки и при следующем вызове продолжает работу

async def bulk_save_source_image_by_tag(url):
    # считать прогресс
    # в файле записана последняя проверенная страница
    global LAST_PAGE_CHECKED
    LAST_PAGE_CHECKED = url
    name = getName(url)

    if name in {"all", "best", "new"}:
        print(str.format("убираем {0}...", name))
        name = getName(cutLastFrom(url, '/'))
        print(str.format("получаем {0}", name))

    #progress_file_name = os.path.join("temp", f"{name}_bulkSaveSrc_imageFromTag.txt")
    progress_file_name = f"output/{name}_lastpage.txt"
    if not os.path.exists("output"):
        os.mkdir("output")

    output_name = f"output/url_{name}.txt"
    if os.path.isfile(progress_file_name):  # если файла нет, то и прогресс не надо считывать
        print("найден файл прогресса")
        with open(progress_file_name, "r") as f:
            LAST_PAGE_CHECKED = f.read()
    else:
        print("файл прогресса не найден")

    if LAST_PAGE_CHECKED == "":
        LAST_PAGE_CHECKED = url
        print("файл прогресса пуст")
    else:
        print("продолжаем с ", LAST_PAGE_CHECKED)

    # продолжить
    async with ClientSession() as session:
        html = await download_parsed_page(LAST_PAGE_CHECKED, session)
        tag_pages_list = getPrevPages(url, html)
        queue = asyncio.Queue()
        producers = [asyncio.create_task(download_and_parse(page, session, queue)) for page in tag_pages_list]
        file_loader = asyncio.create_task(load_parsed_data_to_file(queue, output_name))
        await asyncio.gather(*producers)
        await queue.join()
        file_loader.cancel()
        await asyncio.gather(file_loader, return_exceptions=True)

async def load_parsed_data_to_file(queue, output_name):
    global LAST_PAGE_CHECKED
    while True:
        src_list, censored_list, page = await queue.get()
        print(str.format("Начата обработка страницы {0}", page))
        LAST_PAGE_CHECKED = page
        # следующий кусок кода независимый друг от друга и мы можем выполнить их паралельно
        await asyncio.gather(*[
            append_to_file(src_list, output_name),
            append_to_file(censored_list, "output/censored.txt")
        ])
        print(str.format("Страница {0} обработана", page))
        queue.task_done()

async def download_and_parse(page, session, queue):
    html = await download_parsed_page(page, session)
    result = scrapPage(html)
    src_list = result['links']
    censored_list = result['censored']
    await queue.put((src_list, censored_list, page))

# Запрашивает страницу по адресу
async def download_parsed_page(url, session):
    html_text = await fetch_html(url, session)
    html = parse_html(html_text)
    return html

if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # main_task = asyncio.ensure_future(bulk_save_source_image_by_tag("http://old.reactor.cc/tag/latenight/all"))
    # signal.signal(SIGINT, lambda a,b: main_task.cancel)
    # signal.signal(SIGTERM, lambda a,b: main_task.cancel)
    # try:
    #     loop.run_until_complete(main_task)
    # finally:
    #     loop.close()
    url_to_download = "http://old.reactor.cc/tag/latenight/all"
    try:
        asyncio.run(bulk_save_source_image_by_tag(url_to_download))
    except KeyboardInterrupt:
        name = getName(url_to_download)

        if name in {"all", "best", "new"}:
            name = getName(cutLastFrom(url_to_download, '/'))

        progress_file_name = f"output/{name}_lastpage.txt"
        with open(progress_file_name, "w") as f:
            print(f"Последняя страница ", LAST_PAGE_CHECKED, " сохранена")
            f.write(LAST_PAGE_CHECKED)

