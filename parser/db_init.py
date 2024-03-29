import aiomysql
import pymysql
import os.path
from getpass import getpass

# инициализирует БД
# возвращает пул подключений
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
        pool = await aiomysql.create_pool(host=host, user=user, password=password, db=database, autocommit=True)
        conn = await pool.acquire()
        cur = await conn.cursor()
        await cur.execute("use kl;")
        await cur.close()
        return pool
    except RuntimeError:
        print(f"Ошибка при подключении к базе данных. Проверьте логин и пароль, удостоверьтесь, что база данных доступна.")
        return None

# синхронная версия
# возвращает объект подключения, а не пул подключений, как асинхронная версия
def init_sync():
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
        conn = pymysql.connect(host=host, user=user, password=password, db=database, autocommit=True)
        cur = conn.cursor()
        cur.execute("SET NAMES 'utf8';")
        cur.execute("SET CHARACTER SET 'utf8'")
        cur.execute("SET SESSION collation_connection = 'utf8_general_ci'")
        cur.execute("use kl;")
        cur.close()
        return conn
    except RuntimeError:
        print(f"Ошибка при подключении к базе данных. Проверьте логин и пароль, удостоверьтесь, что база данных доступна.")
        return None

def write_query_results(query, filename):
    con = init_sync()
    cur = con.cursor()
    cur.execute(query)
    result = cur.fetchall()
    with open(filename, "w", encoding="utf-8") as f:
        for row in result:
            for el in row:
                f.write(el)
                f.write(" ")
            f.write("\n")