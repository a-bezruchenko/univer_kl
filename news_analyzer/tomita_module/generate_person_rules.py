import sys

import iuliia

sys.path.append("../../parser/")
from db_init import init_sync



def prepare_rules(full_name):
    parts_count = full_name.count(" ")
    if parts_count == 2:
        return prepare_rules_3(full_name)
    elif parts_count == 1:
        return prepare_rules_2(full_name)
    else:
        print(f"Проверьте имя: {full_name}")
        return ""

# выдать правила грамматики для случая, когда даны три части имени
def prepare_rules_3(full_name):
    family_name, name, father_name = full_name.split(" ")
    family_name, name, father_name = family_name.lower(), name.lower(), father_name.lower()
    t_name = iuliia.translate(full_name, iuliia.Schemas.get("wikipedia")).replace(" ","")
    return (f"""PersonFullName -> {t_name}_familyname {t_name}_name {t_name}_fathername |
{t_name}_familyname {t_name}_name | 
{t_name}_name {t_name}_familyname |
{t_name}_familyname;
{t_name}_familyname -> "{family_name}" interp (Person.FamilyName);
{t_name}_name -> "{name}" interp (Person.Name);
{t_name}_fathername -> "{father_name}" interp (Person.FatherName);
""")

# выдать правила грамматики для случая, когда даны две части имени
def prepare_rules_2(full_name):
    family_name, name = full_name.split(" ")
    family_name, name = family_name.lower(), name.lower()
    t_name = iuliia.translate(full_name, iuliia.Schemas.get("wikipedia")).replace(" ","")
    return (f"""PersonFullName -> {t_name}_familyname {t_name}_name | 
{t_name}_name {t_name}_familyname |
{t_name}_familyname;
{t_name}_familyname -> "{family_name}" interp (Person.FamilyName);
{t_name}_name -> "{name}" interp (Person.Name);
""")

if __name__ == '__main__':
    with init_sync() as cur:
        with open("persons.cxx", "w", encoding="utf-8") as f:
            cur.execute("SELECT fullName FROM persons;")
            f.write('#encoding "utf-8"\n#GRAMMAR_ROOT PersonFullName\n\n')
            for full_name in cur.fetchall():
                full_name = full_name[0]
                rule = prepare_rules(full_name)
                if rule != "":
                    f.write(rule)

