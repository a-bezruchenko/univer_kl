import asyncio
import aiomysql
from db import *
data = {'link': '/text/health/69286435/', 'viewsCount': 298, 'commentsCount': 2}

loop = asyncio.get_event_loop()
con, cur = loop.run_until_complete(init())
loop.run_until_complete(insert_db(data, cur, con))
con.close()