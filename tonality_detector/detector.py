from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
import sys

sys.path.append("../parser/")
from db_init import *


tonality_to_russian = {
    'neutral': 'Нейтральный',
    'negative': 'Негативный',
    'positive': 'Позитивный',
    'speech': 'Речь',
    'skip': 'Не выявлено'
}


def insert_tonality(con, id_filtered, tonality):
    with con.cursor() as cur:
        cur.execute("INSERT INTO tonality (id_filtered, first_tonality, "
                    "first_value, second_tonality, second_value) VALUES (%s, %s, %s, %s, %s);",
                    (id_filtered, tonality_to_russian[tonality[0][0]], float(tonality[0][1]),
                     tonality_to_russian[tonality[1][0]], float(tonality[1][1])))


def print_tonality(text, tonality):
    print(text + "\nТональность текста:")
    for ton in tonality:
        print(tonality_to_russian[ton[0]] + " " + ton[1])


def main():
    db_con = init_sync()
    tokenizer = RegexTokenizer()
    model = FastTextSocialNetworkModel(tokenizer=tokenizer)
    with db_con:
        cur = db_con.cursor()
        # Запрос к предложениям выдленным томитой
        cur.execute("SELECT id, text FROM filtered WHERE text IS NOT NULL")

        filtreds = [{x[0]: x[1]} for x in cur.fetchall() if len(x[1]) > 0]
        tonality = []


        for filtred in filtreds:
            results = model.predict(filtred.values(), k=2)
            for i, el in enumerate(zip(filtred.values(), results)):
                token, sentiment = el
                tonality.clear()
                for key, value in filtred.items():
                    id_filtered = key
                    text = value
                for item in sentiment.items():
                    tonality.append(item)
                insert_tonality(db_con, id_filtered, tonality)
                print_tonality(text, tonality)


if __name__ == '__main__':
    main()
