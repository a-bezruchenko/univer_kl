import aiomysql
import os.path
from getpass import getpass

# инициализирует БД, возвращает объект подключения
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