from pprint import pprint

from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
import sys

sys.path.append("../parser/")
from db_init import *

# test = [
#     '''Ужасное расположение и распределение товаров. Два уровня и на каждом свои кассы. '
#     'Чтобы купить разные группы товаров нужно отстоять две очереди.''',
#     '''Это не шаурма это ужас,куча майонеза,лук одна кожура верхний слой который мы '
#     'при готовке выкладываем,картофель фри из пачек сухой, мясо порезано тонкими '
#     'пластами, не пойму как оно приготавливалось явно не на гриле, мясо было не свежее, '
#     'в итоге самый съедобный оказался лаваш, не рекомендую.''',
#     '''Рядом с домом, вкусная картошечка и обалденные молочные коктейли и '
#     'довольно быстрое обслуживание, приятные кассиры''',
#     '''Замечательный телефон, пользуюсь им уже 2 года, очень нравится!''']


def main():
    db_con = init_sync()
    tokenizer = RegexTokenizer()
    model = FastTextSocialNetworkModel(tokenizer=tokenizer)
    sentences = []
    i = 0
    with db_con:
        cur = db_con.cursor()
        # Запрос к предложениям выдленным томитой
        cur.execute("SELECT text FROM filtered WHERE text IS NOT NULL")

        for sentence in cur.fetchall():
            if len(sentence[0]) > 0:
                sentences.append(sentence[0])

        results = model.predict(sentences, k=2)
        for i, el in enumerate(zip(sentences, results)):
            token, sentiment = el
            print(sentences[i])
            pprint({word: key for key, words in sentiment.items() for word in words})


if __name__ == '__main__':
    main()
