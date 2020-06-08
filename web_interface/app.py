import sys
from flask import Flask, render_template

sys.path.append("../parser/")
from db_init import *

app = Flask(__name__)


@app.route('/')
def index():
    db_con = init_sync()
    with db_con:
        cur = db_con.cursor()
        # Берем статьи из БД
        cur.execute("SELECT * FROM storage WHERE text IS NOT NULL")
        return render_template('index.html', articles=cur.fetchall())


if __name__ == "__main__":
    app.run()
