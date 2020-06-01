# coding: utf8
import asyncio
from aiohttp import ClientSession

from time import time as current_time
from time import sleep
import requests

from fake_useragent import UserAgent

# файл для запросов к серверу

LAST_REQUEST_TIME = current_time()
DEFAULT_WAIT_TIME = 1.0
SAFE_GET_LOCK = asyncio.Lock()


async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    resp = await safe_get(url, session, **kwargs)
    html = await resp.text()
    return html


# Делает запрос с учётом времени между запросами
async def safe_get(url, session, wait_time=DEFAULT_WAIT_TIME, **kwargs):
    global LAST_REQUEST_TIME, SAFE_GET_LOCK
    sleep_time = 0
    async with SAFE_GET_LOCK:
        if current_time() - LAST_REQUEST_TIME < wait_time:
            sleep_time = LAST_REQUEST_TIME + wait_time - current_time()

        LAST_REQUEST_TIME = LAST_REQUEST_TIME + wait_time
    if sleep_time > 0:
        #print(sleep_time)
        await asyncio.sleep(sleep_time)
    print(str.format("Запрашиваем {0}, время:{1}", url, current_time()))
    return await session.request(method="GET", url=url, raise_for_status=True, headers={'User-Agent': UserAgent().chrome}, **kwargs)

def fetch_html_sync(url: str, **kwargs) -> str:
    resp = safe_get_sync(url, **kwargs)
    html = resp.text()
    return html

def safe_get_sync(url, wait_time=DEFAULT_WAIT_TIME):
    global LAST_REQUEST_TIME
    if "LAST_REQUEST_TIME" in globals() and current_time() - LAST_REQUEST_TIME < wait_time:
        LAST_REQUEST_TIME = current_time() + LAST_REQUEST_TIME
        sleep(current_time() - LAST_REQUEST_TIME)
    return requests.get(url=url, headers={'User-Agent': UserAgent().chrome})