import asyncio
from aiohttp import ClientSession, ClientResponseError

from safe_get import fetch_html
from util import getLastFrom

import db
from parser_funcs import parse_html

def get_urls():
    return ["https://global-volgograd.ru/person?offset="+str(offset) for offset in range(0, 180, 20)]

def parse_page(html):
    persons = list(map(lambda x: x.find("div", class_="title").text, html.findAll("div", class_="person-block")))
    persons = list(map(normalize_person_fullname, persons))
    return persons

def start_upper(word):
    if len(word)<2:
        print(word)
        return word.upper()
    else:
        return (word[0].upper())+(word[1:].lower())

def normalize_person_fullname(fullname):
    fullname = fullname.replace("\n", "").lstrip(" ").rstrip(" ")
    parts = list(filter(lambda x: x!="", fullname.split(" ")))
    parts = list(map(start_upper, parts))
    return " ".join(parts)

async def download_and_parse(urls, session, queue):
    for url in urls:
        try:
            html_text = await fetch_html(url, session)
        except ClientResponseError:
            print("Ошибка при обращении к " + url)
            continue
        html = parse_html(html_text)
        result = parse_page(html)
        num = getLastFrom(url, "=")
        await queue.put((result, num))
    await queue.put(True)

async def add_values(data, pool):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO persons (fullname) VALUES (%s);", (data))

async def load_parsed_data_to_db(queue, con):
    while True:
        q_data = await queue.get()
        if q_data == True:
            break
        data_list, num = q_data
        await asyncio.gather(*[add_values(el, con) for el in data_list])
        print(f"Страница {num} обработана")
        queue.task_done()

async def get_persons():
    db_con = await db.init()
    async with ClientSession() as session:
        queue = asyncio.Queue()
        pages_list = get_urls()
        producer = asyncio.create_task(download_and_parse(pages_list, session, queue)) 
        consumer = asyncio.create_task(load_parsed_data_to_db(queue, db_con))
        await asyncio.gather(producer, consumer)
    
if __name__ == "__main__":
    asyncio.run(get_persons())