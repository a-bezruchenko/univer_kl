# coding: utf8
from pprint import pprint
import requests
from bs4 import BeautifulSoup as BS
from parser_funcs import *
from time import sleep

url = "https://v1.ru/text/"
r = requests.get(url)  
parsed_content = parse_html(r.text)
print("get_pages_count:")
print(get_pages_count(parsed_content))
print("quick_scrap_news_page:")
pprint(quick_scrap_news_page(parsed_content))
print("scrap_news_page:")
pprint(scrap_news_page(parsed_content))

sleep(2)

url = "https://v1.ru/text/food/69284848/"
r = requests.get(url)  
parsed_content = parse_html(r.text)
print("scrapPostPage:")
pprint(scrapPostPage(parsed_content))