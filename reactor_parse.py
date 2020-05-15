from bs4 import BeautifulSoup as BS

from util import getLastFrom, cutLastFrom

def parse_html(text):
    return BS(text, 'html.parser')

# формат: {"name", 
# "date",
# "link",
# "text",
# "videoLinks",
# "imgLinks",
# "viewsCount",
# "commentsCount",
# "tags"}
# собираем данные со страницы ленты
def scrapNewsPage(parsed_content):

    posts = parsed_content.findAll("article")
    res = []
    for post in posts:
        post_link = post.find("a", class_="H1al7")['href']
        post_name = post.find("a", class_="H1b1")
        central-column-container
    # link_arr = []
    # censored_arr = []
    # for post in posts:
    #     post_link = post.find("a", class_="link", title="ссылка на пост")['href']
    #     if isPostCensored(post):
    #         censored_arr.append(post_link)
    #     else:
    #         src = getSrcFromPostBlock(post)
    #         if src is not None:
    #             link_arr += src
    # return {"links":link_arr, "censored":censored_arr}

# собираем данные со страницы поста
def scrapPostPage(parsed_content):


# проверяет, запрещён ли пост в россии
def isPostCensored(post):
    return post.find("img", src="/images/censorship/ru.png") is not None

# Получает список соусов из тега с постом
# Варианты:
# Одно или несколько изображений
# Каждое может быть в полной или урезанной версии
# Может быть цензура (не обрабатывается)
def getSrcFromPostBlock(post):
    try:
        image_tags = post.findAll("div", class_="image")
        src = []
        if not image_tags:
            return None
        else:
            for tag in image_tags:
                if tag.find("a", class_="prettyPhotoLink") is not None:
                    src.append(tag.find("a", class_="prettyPhotoLink")['href'])
                elif tag.img is not None:
                    src.append(tag.img['src'])
                elif tag.find("span", class_="more_content") is not None:
                    continue
                else:
                    print("Не удалось извлечь ссылку: " + tag.prettify())
            return src
    except (TypeError): # хз, какие ещё случаи бывают, пусть пишется
        print("Не удалось получить ссылку из поста: " + post.prettify())
        return None

# По url и тексту страницы ленты составляет список предыдущих страниц
def getPrevPages(url, parsed_content):
    name = getLastFrom(url, '/')
    stopNumber = None
    if name.isdigit():
        stopNumber = int(name)
        url = cutLastFrom(url, '/')
    url += '/'
    if stopNumber is None:
        # выясняем максимальный номер страницы
        next_button = parsed_content.findAll("a", class_="next")
        if 0 == len(next_button):
            stopNumber = -1  # Цикл далее не начнется
        else:
            stopNumber = int(getLastFrom(next_button[0]['href'], '/'))
    for i in range(stopNumber + 1, 0, -1):
        yield url + str(i)