import asyncio
import aiomysql
from db import *

data = {'link': '/text/health/69286435/', 'viewsCount': 298, 'commentsCount': 2}
loop = asyncio.get_event_loop()
con = loop.run_until_complete(init())
loop.run_until_complete(add_values(data, con))
data['viewsCount'] = 100500
loop.run_until_complete(add_values(data, con))
con.close()
