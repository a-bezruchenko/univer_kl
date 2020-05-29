import asyncio
import aiomysql
from db import *
data = {'link': '/text/health/69286435/','viewsCount': 298,'commentsCount': 2}

async def temp1(con, cur):
    print("start")
    await cur.execute("""INSERT INTO `kl`.`Storage` (link, title, date, section, theme, text, viewsCount, commentsCount)
VALUES ("/text/health/69286435/", null, null, null, null, null, 298, 2);""")
    await cur.execute("SELECT * from storage")
    await con.commit()
    r = await cur.fetchall()
    print(r)
    print("end")

loop = asyncio.get_event_loop()
con, cur = loop.run_until_complete(init())
loop.run_until_complete(temp1(con, cur))
con.close()
#loop.run_until_complete(insert_db(data, cur, con))
#loop.close()