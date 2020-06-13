# coding: utf8
import subprocess
import os
import re
import sys
from pprint import pprint
from db_init import init_sync

def find_facts(text, base_path = "./", path_to_tomita = "./tomita-parser"):
    raw_result = analyse_text_with_tomita(text, base_path=base_path, path_to_tomita=path_to_tomita)
    res = []
    regexp = r"(.*)\n\s+Person\n\s+\{((?:\n\s+\s+(?:Name|FamilyName|FatherName) = .*?)+\n\s+\})"
    for find_res in re.findall(regexp, raw_result):
        res.append(find_res[0])
    regexp = r"(.*)\n\s+Place\n\s+\{((?:\n\s+\s+(?:Name) = .*?)+\n\s+\})"
    for find_res in re.findall(regexp, raw_result):
        res.append(find_res[0])
    return res

def analyse_text_with_tomita(text, base_path = "./", path_to_tomita = "./tomita-parser", rewrite_config=True):
    input_file_name = base_path+"input_py"
    output_file_name = base_path+"output_py"
    config_file_name = base_path+"config_py.proto"
    if rewrite_config:
        config_content = """
encoding "utf8";

TTextMinerConfig {
  Dictionary = "mydic.gzt";

  Input = {
    File = "input_py"; 
  }

  Articles = [
    { Name = "персоны" },
    { Name = "достопримечательности" }
  ]

  Facts = [
    { Name = "Person" },
    { Name = "Place" }
  ]

  Output = {
    File = "output_py";
    Format = text;
  }
}
"""
        with open(config_file_name, "w", encoding="utf-8") as c_f:
            c_f.write(config_content)
    with open(input_file_name, "w", encoding="utf-8") as i_f:
        i_f.write(text)
    subprocess.call([path_to_tomita, config_file_name])
    with open(output_file_name, "r", encoding="utf-8") as o_f:
        output = o_f.read()
    os.remove(input_file_name)
    os.remove(output_file_name)
    if rewrite_config:
        os.remove(config_file_name)
    return output
    
if __name__ == '__main__':
    if len(sys.argv) == 1:
        PATH_TO_TOMITA = "./tomita-parser"
        BASE_PATH = "./"
    elif len(sys.argv) == 2:
        PATH_TO_TOMITA = sys.argv[1]
        BASE_PATH = "./"
    else:
        PATH_TO_TOMITA = sys.argv[1]
        BASE_PATH = sys.argv[2]
    print("Путь к томите: " + PATH_TO_TOMITA)
    print("Путь к файлам грамматики: " + BASE_PATH)
    con = init_sync()
    print("Начинаю обрабатывать...")
    with con.cursor() as cur:
        cur.execute(f'SELECT count(*) FROM storage;')
        db_size = cur.fetchall()[0][0]
        batch_size = 50
        for offset in range(0, db_size-db_size%batch_size, batch_size):
            cur.execute(f'SELECT link, text FROM storage LIMIT {batch_size} OFFSET {offset};')
            rows = cur.fetchall()
            text = '\n'.join(list(map(lambda x:x[1], rows)))
            res = find_facts(text, base_path=BASE_PATH, path_to_tomita=PATH_TO_TOMITA)
            if res != []:
                for el in res:
                    el = str(el)
                    el = (el.replace(" .", ".")
                        .replace(" ,", ",")
                        .replace(" ;", ";")
                        .replace(" :", ":")
                        .replace(" -", "-")
                        .replace(" —", "—"))
                    link_to_insert = ""
                    for row in rows:
                        link, text = row
                        if text.replace("«", '"').replace("»", '"').replace(" ", "").find(el.replace(" ", "")) != -1:
                            link_to_insert = link
                            break
                    if len(el) > 0 and link_to_insert != "":
                        cur.execute('INSERT INTO filtered (link, text) values (%s, %s);', (link_to_insert, el))
                    elif link_to_insert == "":
                        print("Не удалось найти статью:")
                        print(el)
            print(f"Первые {offset+batch_size} записей обработаны")
    print("Данные обработаны")
