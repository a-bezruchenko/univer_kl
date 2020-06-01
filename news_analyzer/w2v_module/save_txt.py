def save_text_db_to_txt(con):
    filename = "text"
    i = 1

    with con:
        cur = con.cursor()
        # Берем тексты статей из БД
        cur.execute("SELECT text FROM storage WHERE text IS NOT NULL")

        # Сохраняем в файлы для обучения модели
        for el in cur.fetchall():
            output_file = open(f'./data_text/{filename}_{i}.txt', 'w')
            i += 1
            output_file.write(el[0])
            output_file.close()
