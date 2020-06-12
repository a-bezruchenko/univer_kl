import subprocess
import os
import re
import sys
from pprint import pprint
from db_init import init_sync

def find_facts(text):
    raw_result = analyse_text_with_tomita(text)
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
    con = init_sync()
    print("Начинаю обрабатывать...")
    with con.cursor() as cur:
        cur.execute(f'SELECT count(*) FROM storage;')
        db_size = cur.fetchall()[0][0]
        batch_size = 100
        for limit in [(x,batch_size) for x in range(0, db_size-db_size%batch_size)]:
            cur.execute(f'SELECT link, text FROM storage LIMIT {limit[0]}, {limit[1]};')
            for row in cur.fetchall():
                link, text = row
                res = find_facts(text)
                if res != []:
                    for el in res:
                        el = str(el)
                        if len(el) > 0:
                            cur.execute('INSERT INTO filtered (link, text) values (%s, %s);', (link, el))
                print(f"{link} обработана")
    print("Данные обработаны")
