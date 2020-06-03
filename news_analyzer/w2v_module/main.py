PATH = 'model/kurs_model/'

from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2VecModel
from pprint import pprint
import save_txt
import word2vec
import os
from get_objects import *
import sys
sys.path.append("../../parser/")
from db_init import *


def get_synonyms(elements, count, model, spark_session):
    result = []
    for element in elements:
        try:
            elementDF = spark_session.createDataFrame([
                (element[0].lower().split(" "),)], ["words"])
            transform_elem = model.transform(elementDF)
            synonyms = model.findSynonyms(transform_elem.collect()[0][1], count).collect()
            result.append(synonyms)
        except Exception:
            result.append("Синонимы не найдены")

    return result



def main():
    db_con = init_sync()
    if(not os.path.exists('model')):
        if (not os.path.exists('data_text')):
            print("Папка создана")
            os.mkdir('data_text')
        save_txt.save_text_db_to_txt(db_con)

        word2vec.create_w2v_model()

    persons = get_persons(db_con)
    places = get_places(db_con)

    spark = SparkSession \
        .builder \
        .appName("SimpleApplication") \
        .getOrCreate()

    model = Word2VecModel.load(PATH)

    pprint("Поиск контекстных синонимов персон:")
    persons_synonyms = get_synonyms(persons, 5, model, spark)
    pprint(len(persons_synonyms))
    for i in range(len(persons_synonyms)):
        pprint("-" * 30)
        pprint(persons[i])
        pprint(persons_synonyms[i])

    spark.stop()

if __name__ == '__main__':
    main()