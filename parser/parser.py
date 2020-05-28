# encode: utf-8
# этот файл содержит функции парсинга различных видов страниц
import requests
from bs4 import BeautifulSoup as BS
from util import intTryParse, tryFunction

# формат: список ссылок
def quick_scrap_news_page(parsed_content):
    return list(map(
                lambda x: x.find("a")['href'],
                parsed_content.find("div", class_="central-column-container").findAll("article")))

# формат: [{"link", "viewsCount", "likesCount"}]
def scrap_news_page(parsed_content):
    news_column = parsed_content.find("div", class_="central-column-container")
    posts = news_column.findAll("article")
    overall_result = []
    for post in posts:
        try:
            temp_res = {}
            temp_res["link"] = post.findAll("a")[0]['href']
            #temp_res["viewsCount"] = intTryParse(post.findAll("span")[0].text, 0)
            #temp_res["commentsCount"] = intTryParse(post.findAll("span")[1].text, 0)
            temp_res["viewsCount"] = tryFunction(lambda: int(post.findAll("span")[0].text.replace("\xa0", "")), 0)
            temp_res["commentsCount"] = tryFunction(lambda: int(post.findAll("span")[1].text.replace("\xa0", "")), 0)
            overall_result.append(temp_res)
        except (AttributeError, KeyError, TypeError):
            print("info: не удалось извлечь ссылку")
    return overall_result

# формат: {"title", 
# 
# "date",
# "link",
# "section",
# "theme",
# "format",
# "text",
# "videoLinks",
# "imgLinks",
# "viewsCount",
# "commentsCount"}
def scrapPostPage(parsed_content):
    header = parsed_content.select_one("#record-header")
    result = {}
    result["title"] = list(list(header.children)[0].find("h2", class_="I3akh I3amf BZb1").children)[0]["title"].lstrip(" ")
    result["link"] = list(list(header.children)[0].find("h2", class_="I3akh I3amf BZb1").children)[0]["href"]
    result["datetime"] = list(header.children)[0].find("div", class_="I3akv BZj3")["datetime"]
    try:
        result["section"] = list(header.children)[0].find("a", class_="I3ak1 I3amn BZj7").text.lstrip(" ").rstrip(" ")
    except (AttributeError, KeyError, TypeError):
        pass
    
    try:
        result["theme"] = list(header.children)[0].find("a", class_="I3ak5 I3amh BZj9").text.lstrip(" ").rstrip(" ")
    except (AttributeError, KeyError, TypeError):
        pass
    
    try:
        result["format"] = list(header.children)[0].find("a", class_="I3ak1 I3amn BZj-").text.lstrip(" ").rstrip(" ")
    except (AttributeError, KeyError, TypeError):
        pass

    result["commentsCount"] = int(list(header.children)[1].find("a", class_="LHd- LHe5").text)
    result["viewsCount"] = int(list(header.children)[1].find("div", class_="LHd-").text.replace('\xa0', ''))

    result["text"] = ' '.join(list(map(lambda x:x.text, parsed_content.find("div", itemprop="articleBody").findAll("p"))))

