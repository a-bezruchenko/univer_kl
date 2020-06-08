import sys
sys.path.append("../../parser/")
from db_init import init_sync
sys.path.append("../w2v_module/")
from save_txt import save_text_db_to_txt

if __name__ == '__main__':
    db_con = init_sync()
    save_text_db_to_txt(db_con, save_to_one_file=True, filename_base="input")
