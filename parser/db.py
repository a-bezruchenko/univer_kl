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
        con = await aiomysql.connect(host=host, user=user, password=password, db=database, autocommit=True)
        cur = await con.cursor()
        await cur.execute("use kl;")
        return con, cur
    except RuntimeError:
        print(f"Ошибка при подключении к базе данных. Проверьте логин и пароль, удостоверьтесь, что база данных доступна.")
        return None

# вставляет новую запись без проверки уникальности
# принимает словарь
async def insert_db(data, cur, con):
    link = data['link']
    title = tryFunction(lambda: data['title'], None)
    date = tryFunction(lambda: data['date'], None)
    section = tryFunction(lambda: data['section'], None)
    theme = tryFunction(lambda: data['theme'], None)
    text = tryFunction(lambda: data['text'], None)
    viewsCount = tryFunction(lambda: int(data['viewsCount']), None)
    commentsCount = tryFunction(lambda: int(data['commentsCount']), None)
    print((link, title, date, section, theme, text, viewsCount, commentsCount))
    await cur.execute("INSERT INTO `kl`.`Storage` (link, title, date, section, theme, text, viewsCount, commentsCount) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
 (link, title, date, section, theme, text, viewsCount, commentsCount))
    await cur.execute("COMMIT;")

async def select_from_db(link, cur, con):
    await cur.execute("SELECT * FROM Storage WHERE link=%s", (link,))
    return await cur.fetchall()

# обновляет записи без проверки существования
# принимает словарь
async def update_db(data, cur, con):
    link = data['link']
    title = tryFunction(lambda: data['title'], None)
    date = tryFunction(lambda: data['date'], None)
    section = tryFunction(lambda: data['section'], None)
    theme = tryFunction(lambda: data['theme'], None)
    text = tryFunction(lambda: data['text'], None)
    viewsCount = tryFunction(lambda: int(data['viewsCount']), None)
    commentsCount = tryFunction(lambda: int(data['commentsCount']), None)
    args_str = []
    if title is not None: args_str.append("title=%s") 
    if date is not None: args_str.append("date=%s") 
    if section is not None: args_str.append("section=%s") 
    if theme is not None: args_str.append("theme=%s") 
    if text is not None: args_str.append("text=%s") 
    if viewsCount is not None: args_str.append("viewsCount=%s") 
    if commentsCount is not None: args_str.append("commentsCount=%s")
    query = "UPDATE Storage SET " + ', '.join(args_str) + " WHERE link = %s;"
    args = tuple(filter(None, (title, date, section, theme, text, viewsCount, commentsCount, link)))
    print(query)
    print(args)
    await cur.execute(query, args)
    await cur.execute("COMMIT;")