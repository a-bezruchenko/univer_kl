import pymysql

PATH = 'model/kurs_model/'

from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2VecModel
from pprint import pprint
import save_txt
import word2vec
import os
import sys
sys.path.append("../../parser/")
from db_init import *

def main():
    if(not os.path.exists('model')):
        db_con = pymysql.connect('localhost', 'root',
                      'password', 'kl')
        if (not os.path.exists('data')):
            print("Папка создана")
            os.mkdir('data')
        save_txt.save_text_db_to_txt(db_con)

        word2vec.create_w2v_model()

    spark = SparkSession \
        .builder \
        .appName("SimpleApplication") \
        .getOrCreate()

    model = Word2VecModel.load(PATH)

    print("Ищу синонимы")
    pprint(model.findSynonyms("дом", 5).collect())

    spark.stop()

if __name__ == '__main__':
    main()