import aiomysql
import os.path
from getpass import getpass
from util import tryFunction

async def init():
    filename = "mysql_login_data.txt"
    if os.path.isfile(filename):
        print(f"Найден файл данных {filename}")
        with open(filename, "r") as f:
            host = f.readline().replace("\n","")
            user = f.readline().replace("\n","")
            password = f.readline().replace("\n","")
            database = f.readline().replace("\n","")
    else:
        print(f"Файл {filename} не обнаружен")
        print("Введите хост:")
        host = input()
        print("Введите логин:")
        user = input()
        print("Введите пароль:")
        password = getpass()
        print("Введите имя базы данных:")
        database = input()
    try:
        con = await aiomysql.connect(host=host, user=user, password=password, db=database)
        cur = await con.cursor()
        await cur.execute("use kl;")
        return con, cur
    except RuntimeError:
        print(f"Ошибка при подключении к базе данных. Проверьте логин и пароль, удостоверьтесь, что база данных доступна.")
        return None

# вставляет новую запись без проверки уникальности
# принимает словарь
async def insert_db(data, cur, con):
    link = con.escape(data['link'])
    title = tryFunction(lambda: con.escape(data['title']), None)
    date = tryFunction(lambda: data['date'], None)
    section = tryFunction(lambda: con.escape(data['section']), None)
    theme = tryFunction(lambda: con.escape(data['theme']), None)
    text = tryFunction(lambda: con.escape(data['text']), None)
    viewsCount = tryFunction(lambda: int(data['viewsCount']), None)
    commentsCount = tryFunction(lambda: int(data['commentsCount']), None)
    print("start query")
    query = """
INSERT INTO `Storage` (link, title, date, section, theme, text, viewsCount, commentsCount)
VALUES ("%s", %s, %s, %s, %s, %s, %s, %s);"""
    await cur.execute(query, (link, title, date, section, theme, text, viewsCount, commentsCount))
    await con.commit()
    print("end query")

# обновляет записи без проверки существования
# принимает словарь
async def update_db(data, cur, con):
    query = """
UPDATE `Order` SET State=%s WHERE id=<>"""
    link = con.escape(data['link'])
    title = tryFunction(lambda: con.escape(data['title']), None)
    date = tryFunction(lambda: data['date'], None)
    section = tryFunction(lambda: con.escape(data['section']), None)
    theme = tryFunction(lambda: con.escape(data['theme']), None)
    text = tryFunction(lambda: con.escape(data['text']), None)
    viewsCount = tryFunction(lambda: int(data['viewsCount']), None)
    commentsCount = tryFunction(lambda: int(data['commentsCount']), None)

        


