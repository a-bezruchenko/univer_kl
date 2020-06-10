import sys

sys.path.append("../../parser/")
from db_init import init_sync

def prepare_rules(raw_name):
    splitted_name = raw_name.split(" ")
    processed_splitted_name = list(map(lambda x: '"' + x.replace('"', '').lower() + '"', splitted_name))
    final_name = ' '.join(processed_splitted_name)
    return (f'Place -> {final_name};\n')

if __name__ == '__main__':
    with init_sync() as cur:
        with open("places.cxx", "w", encoding="utf-8") as f:
            cur.execute("SELECT name FROM places;")
            f.write('#encoding "utf-8"\n#GRAMMAR_ROOT PlaceName\n\nPlaceName -> Place interp (Place.Name);\n')
            for name in cur.fetchall():
                name = name[0]
                rule = prepare_rules(name)
                if rule != "":
                    f.write(rule)
