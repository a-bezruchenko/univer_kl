import asyncio
import aiomysql
from db import *
from db_parser import *

data = {'link': '/text/health/69286435/', 'viewsCount': 298, 'commentsCount': 2}
loop = asyncio.get_event_loop()
con = loop.run_until_complete(init())
loop.run_until_complete(add_values(data, con))
data['viewsCount'] = 100500
data['date'] = "2020-05-29 09:00:00"
loop.run_until_complete(add_values(data, con))
print(loop.run_until_complete(get_incomplete_records(con))) #(('/text/health/69286435/',),)
con.close()