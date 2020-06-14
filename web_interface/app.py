import sys
from flask import Flask, render_template, request
from flask_paginate import Pagination

sys.path.append("../parser/")
from db_init import *

app = Flask(__name__)

db_con = init_sync()

@app.route('/')
def index():
    with db_con:
        page = int(request.args.get('page', 1))
        per_page = 100
        offset = (page - 1) * per_page

        cur = db_con.cursor()
        cur.execute("SELECT count(*) FROM storage WHERE text IS NOT NULL ")
        size = cur.fetchone()[0]

        # Берем статьи из БД
        cur.execute("SELECT * FROM storage WHERE text IS NOT NULL ORDER BY `date` DESC LIMIT %s OFFSET %s",
                    (per_page, offset))
        pagination = Pagination(page=page, per_page=per_page, total=size, css_framework='bootstrap4')
        return render_template('index.html', articles=cur.fetchall(), page=page, per_page=per_page, pagination=pagination)


@app.route('/getTonality')
def get_tonality():
    with db_con:
        page = int(request.args.get('page', 1))
        per_page = 200
        offset = (page - 1) * per_page

        cur = db_con.cursor()
        cur.execute("SELECT count(*) FROM tonality")
        size = cur.fetchone()[0]

        cur.execute("SELECT f.text, t.first_tonality, t.first_value, t.second_tonality, t.second_value "
                    "FROM `tonality` t INNER JOIN `filtered` f ON f.id = t.id_filtered LIMIT %s OFFSET %s",
                    (per_page, offset))
        pagination = Pagination(page=page, per_page=per_page, total=size, css_framework='bootstrap4')
        return render_template('tonality.html', elements=cur.fetchall(), age=page, per_page=per_page, pagination=pagination)


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
