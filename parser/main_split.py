# coding: utf8
# этот файл — один из исполняемых
# скрипт проходит по таблице Storage, разбивает тексты оттуда на предложения и вставляет в таблицу splitted_data
import db
import db_splitter

def split(text):
    return [el for lst in list(map(lambda x: x.split("  "), text.split(". "))) for el in lst]

if __name__ == "__main__":
    db_con = db.init_sync()
    for el in db_splitter.get_list_of_unsplitted_pages(db_con):
        db_splitter.add_list_to_db(el[0], split(el[1]), db_con)
        print(f"Статья {el[0]} обработана")