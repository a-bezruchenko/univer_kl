import subprocess
import os
import re
import sys
from pprint import pprint
from db_init import init_sync

def find_facts(text):
    raw_result = analyse_text_with_tomita(text)
    res = []
    regexp = r"(.*)\n\tPerson\n\t\{((?:\n\t\t(?:Name|FamilyName|FatherName) = .*?)+\n\t\})"
    for find_res in re.findall(regexp, raw_result):
        line = find_res[0]
        person = {}
        person_data = find_res[1]
        for el in list(map(lambda x:x.replace('\t',''), person_data.split('\n')[1:-1])):
            if el.startswith("Name"):
                person["name"] = el.replace("Name = ", "")
            elif el.startswith("FamilyName"):
                person["familyname"] = el.replace("FamilyName = ", "")
            elif el.startswith("FatherName"):
                person["fathername"] = el.replace("FatherName = ", "")
            else:
                print(f"Ошибка при анализе {el}")
        res.append({"text":line, "person":person})
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
  
  PrettyOutput = "pretty.html"; 

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
    
# if __name__ == '__main__':
#     with open(sys.argv[1], 'r', encoding="utf-8") as f:
#         pprint(find_facts(f.read()))
if __name__ == '__main__':
    con = init_sync()
    with con.cursor() as cur:
        cur.execute("SELECT id, link, text FROM splitted LIMIT 100;")
        for row in cur.fetchall():
            id, link, text = row
            res = find_facts(text)
            if res != []:
                cur.execute("INSERT INTO filtered (id, link, text) values;", (id,link,text))
