import sys
sys.path.append("../../parser/")
from db_init import init_sync
import codecs


# if __name__ == '__main__':
#     filename = "./input.txt"
#     with init_sync() as cur:
#         cur.execute("SELECT id, text FROM splitted WHERE text IS NOT NULL")
#         with codecs.open("dummy", 'w') as dummy_file:
#             with codecs.open(filename, 'w', encoding="utf-8") as output_file:
#                 for el in cur.fetchall():
#                     try:
#                         dummy_file.write(el[1])
#                         output_file.write(el[1])
#                     except UnicodeEncodeError:
#                         print(el[0])
                

if __name__ == '__main__':
    filename = "./input.txt"
    with init_sync() as cur:
        cur.execute("SELECT text FROM storage WHERE text IS NOT NULL LIMIT 250;")
        with codecs.open(filename, 'w', encoding='utf-8') as output_file:
            for el in cur.fetchall():
                output_file.write(el[0])

# if __name__ == '__main__':
#     filename = "./input.txt"
#     with init_sync() as cur:
#         cur.execute("SELECT text FROM storage WHERE text IS NOT NULL")
#         with open(filename, 'w') as output_file: # , encoding='utf-8'
#             for el in cur.fetchall():
#                 for ch in el[0]+'\n':
#                     try:
#                         output_file.write(ch)
#                     except UnicodeEncodeError:
#                         pass