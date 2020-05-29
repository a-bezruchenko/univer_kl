from pprint import pprint
import requests
from bs4 import BeautifulSoup as BS
from parser_funcs import *
url = "https://v1.ru/text/"
r = requests.get(url)  
parsed_content = parse_html(r.text)
print("quick_scrap_news_page:")
pprint(quick_scrap_news_page(parsed_content))
print("scrap_news_page:")
pprint(scrap_news_page(parsed_content))
url = "https://v1.ru/text/food/69284848/"
r = requests.get(url)  
parsed_content = parse_html(r.text)
print("scrapPostPage:")
pprint(scrapPostPage(parsed_content))