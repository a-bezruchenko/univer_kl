PATH = 'model/kurs_model_new/'

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
    for person in persons:
        pprint("-"*30)
        pprint(person[0])
        try:
            # pprint(model.findSynonyms(person[0].split(' ', 1)[0].lower(), 3).collect())
            documentDF = spark.createDataFrame([
                (person[0].lower().split(" "),)], ["words"])
            result = model.transform(documentDF)
            pprint(model.findSynonyms(result.collect()[0][1], 5).collect())
        except Exception:
            pprint("Синонимы не найдены")

    spark.stop()

if __name__ == '__main__':
    main()