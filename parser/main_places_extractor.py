import db_init
from parser_funcs import parse_html

if __name__ == "__main__":
    with open("data/places.html", "r", encoding="utf-8") as f:
        text = f.read()
    parsed_content = parse_html(text)
    ta = parsed_content.find("div", id="afisha-content").findAll("div", class_="ta-f-box ta-f-box-cat")
    places = list(map(
            lambda x: x.findAll("a")[1].text,
            parsed_content.find("div", id="afisha-content").findAll("div", class_="ta-f-box ta-f-box-cat")))
    con = db_init.init_sync()
    cur = con.cursor()
    for place in places:
        cur.execute("INSERT INTO places (name) VALUES (%s);", (place))
