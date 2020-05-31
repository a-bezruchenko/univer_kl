from util import tryFunction

# добавляет или обновляет запись в базе данных
# незаданные поля не трогаются
# вставляет скачанные с сайта данные в таблицу Storage
async def add_values(data, pool):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            data_is_in_db = await is_in_db(data['link'], cur)
            if data_is_in_db:
                await update_db(data, cur)
            else:
                await insert_db(data, cur)

async def get_incomplete_records(pool):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT link FROM Storage WHERE text is null;")
            return await cur.fetchall()

# вставляет новую запись без проверки уникальности
# принимает словарь
async def insert_db(data, cur):
    link = data['link']
    title = tryFunction(lambda: data['title'], None)
    date = tryFunction(lambda: data['date'], None)
    section = tryFunction(lambda: data['section'], None)
    theme = tryFunction(lambda: data['theme'], None)
    text = tryFunction(lambda: data['text'], None)
    viewsCount = tryFunction(lambda: int(data['viewsCount']), None)
    commentsCount = tryFunction(lambda: int(data['commentsCount']), None)
    await cur.execute("INSERT INTO `kl`.`Storage` (link, title, date, section, theme, text, viewsCount, commentsCount) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
 (link, title, date, section, theme, text, viewsCount, commentsCount))
    await cur.execute("COMMIT;")

async def select_from_db(link, cur):
    await cur.execute("SELECT * FROM Storage WHERE link=%s", (link,))
    return await cur.fetchall()

async def is_in_db(link, cur):
    await cur.execute("SELECT COUNT(*) FROM Storage WHERE link=%s", (link,))
    if (await cur.fetchone())[0]==1:
        return True
    else:
        return False

# обновляет запись без проверки существования
# принимает словарь
async def update_db(data, cur):
    if not ('link' in data):
        return 
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
    args = tuple(filter(lambda x: x is not None, (title, date, section, theme, text, viewsCount, commentsCount, link)))
    if len(args)==0:
        return
    await cur.execute(query, args)
    await cur.execute("COMMIT;")