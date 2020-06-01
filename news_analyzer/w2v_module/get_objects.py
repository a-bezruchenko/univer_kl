def get_persons(con):
    with con:
        cur = con.cursor()
        # Берем персон из БД
        cur.execute("SELECT fullname FROM persons WHERE fullname IS NOT NULL")
        return cur.fetchall()


def get_places(con):
    with con:
        cur = con.cursor()
        # Берем персон из БД
        cur.execute("SELECT `name` FROM places WHERE `name` IS NOT NULL")
        return cur.fetchall()