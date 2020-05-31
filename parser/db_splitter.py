def get_list_of_unsplitted_pages(con):
    with con.cursor() as cur:
        cur.execute("SELECT link, text FROM storage WHERE text IS NOT NULL AND link NOT IN (SELECT link FROM splitted);")
        return cur.fetchall()
    
def add_list_to_db(link, texts, con):
    with con.cursor() as cur:
        cur.execute("set autocommit=0;")
        cur.execute("BEGIN;")
        try:
            for text in texts:
                cur.execute("INSERT INTO splitted (link,text) VALUES (%s,%s);", (link, text))
            cur.execute("commit;")
            cur.execute("set autocommit=1;")
        except BaseException as e:
            cur.execute("rollback;")
            raise e