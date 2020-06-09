import sys
from flask import Flask, render_template, request

sys.path.append("../parser/")
from db_init import *

app = Flask(__name__)

db_con = init_sync()

@app.route('/')
def index():
    with db_con:
        cur = db_con.cursor()
        # Берем статьи из БД
        cur.execute("SELECT * FROM storage WHERE text IS NOT NULL")
        return render_template('index.html', articles=cur.fetchall())


@app.route('/getTonality')
def get_tonality():
    return "Здесь будет тональность"


@app.route('/getFacts')
def get_facts():
    return "Здесь будет результат томиты"


@app.route('/getSynonyms', methods=['post', 'get'])
def get_synonyms():
    word = ''
    if request.method == 'POST':
        word = request.form.get('word')

    with db_con:
        cur = db_con.cursor()
        cur.execute("select synonym from places_synonyms where name like %s "
                    "union select synonym from persons_synonyms where fullname like %s",
                    (("%" + word + "%"), ("%" + word + "%")))
    return render_template('synonyms.html', synonyms=cur.fetchall(), word=word)

if __name__ == "__main__":
    app.run()
