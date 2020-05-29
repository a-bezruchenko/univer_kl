# coding: utf8
# этот файл содержит функции парсинга различных видов страниц
from bs4 import BeautifulSoup as BS
from util import tryFunction

def parse_html(text):
    return BS(text, 'html.parser')

# формат: список ссылок
def quick_scrap_news_page(parsed_content):
    return list(map(
                lambda x: x.find("a")['href'],
                parsed_content.find("div", class_="central-column-container").findAll("article")))

# формат: число
def get_pages_count(parsed_content):
    return int(list(parsed_content.findAll("div")[538].children)[-1].text)

# формат: [{"link", "viewsCount", "likesCount"}]
def scrap_news_page(parsed_content):
    news_column = parsed_content.find("div", class_="central-column-container")
    posts = news_column.findAll("article")
    overall_result = []
    for post in posts:
        try:
            temp_res = {}
            temp_res["link"] = post.find("a")['href']
            temp_res["title"] = post.find("h2").text
            # возможно, здесь бы использовать partial, но мне лень
            temp_res["viewsCount"] = tryFunction(lambda: int(post.findAll("span")[0].text.replace("\xa0", "")), 0)
            temp_res["commentsCount"] = tryFunction(lambda: int(post.findAll("span")[1].text.replace("\xa0", "")), 0)
            overall_result.append(temp_res)
        except (AttributeError, KeyError, TypeError):
            print("info: не удалось извлечь ссылку")
    return overall_result



# формат: {"title", 
# "datetime",
# "section",# опционально
# "theme",  # опционально
# "text",
# "viewsCount",
# "commentsCount"}
def scrapPostPage(parsed_content):
    header = parsed_content.select_one("#record-header")
    result = {}
    result["title"] = list(header.children)[0].findAll("h2")[0].text.lstrip(" ").rstrip(" ")
    result["datetime"] = header.find("time")['datetime']
    try:
        result["section"] = list(header.children)[0].findAll("a")[0]['href'].lstrip(" ").rstrip(" ")
    except (AttributeError, KeyError, TypeError):
        pass
    try:
        result["theme"] = list(header.children)[0].findAll("a")[1]['href'].lstrip(" ").rstrip(" ")
    except (AttributeError, KeyError, TypeError):
        pass
    # комменты не берутся, они там реализованы через зад
    result["viewsCount"] = tryFunction(lambda: int(list(header.children)[1].findAll("div")[1].text.replace("\xa0", "")), 0)
    result["text"] = ' '.join(list(map(lambda x: x.text, parsed_content.find("div", itemprop="articleBody").findAll("p")))).replace("\xa0", " ")
    return result