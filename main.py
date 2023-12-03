import psycopg2


def connect_db():
    conn_db = psycopg2.connect(
        host="localhost",
        port="5439",
        database="sql_test",
        user="root",
        password="postgres",
    )
    return conn_db


con = connect_db()
con.set_session(autocommit=True)  # автокоммитинг


def get_vocabulary():
    vocabulary_en = {}
    vocabulary_ru = {}
    vocabulary_id = {}
    cur = con.cursor()
    cur.execute(
        f"""SELECT word_en
                FROM english_words.eng_words_new
                WHERE time_request < now() OR time_request IS NULL 
                ORDER BY id"""
    )
    rows_ = cur.fetchall()
    key_en = 0
    for i in rows_:
        key_en += 1
        vocabulary_en[key_en] = i[0]

    cur.execute(
        f"""SELECT word_ru
                FROM english_words.eng_words_new
                WHERE time_request < now() OR time_request IS NULL 
                ORDER BY id"""
    )
    rows_ = cur.fetchall()
    key_ru = 0
    for i in rows_:
        key_ru += 1
        vocabulary_ru[key_ru] = i[0]

    cur.execute(
        f"""SELECT id
                    FROM english_words.eng_words_new
                    WHERE time_request < now() OR time_request IS NULL 
                    ORDER BY id"""
    )
    rows_ = cur.fetchall()
    key_ru = 0
    for i in rows_:
        key_ru += 1
        vocabulary_id[key_ru] = i[0]
    return vocabulary_en, vocabulary_ru, vocabulary_id  # получаю 3 словаря чтобы=


# НАЧАЛО ================== выбираем временной перенос вызова слова


def change_time_output_again(a):  # временной перенос вызова слова - отсутствует
    cur = con.cursor()
    cur.execute("""UPDATE english_words.eng_words_new  
                    SET time_request = CURRENT_TIMESTAMP
                    WHERE id = %s""", (int(a),))


def change_time_output_easy(a):
    cur = con.cursor()
    cur.execute("""UPDATE english_words.eng_words_new  
                    SET time_request = CURRENT_TIMESTAMP + interval '15 minute'
                    WHERE id = %s""", (int(a),))


def change_time_output_good(a):
    cur = con.cursor()
    cur.execute("""UPDATE english_words.eng_words_new  
                    SET time_request = CURRENT_TIMESTAMP + interval '1 day'
                    WHERE id = %s""", (int(a),))


def change_time_output_hard(a):
    cur = con.cursor()
    cur.execute("""UPDATE english_words.eng_words_new  
                    SET time_request = CURRENT_TIMESTAMP + interval '3 day'
                    WHERE id = %s""", (int(a),))


# КОНЕЦ ================== выбираем временной перенос вызова слова

vocabulary_en, vocabulary_ru, vocabulary_id = get_vocabulary()
w_id = 0


def counter_vocabulary():  # возвращает количество пар слов
    counter = len(vocabulary_id)
    return counter


sequence_number = 0  # счетчик для выборки слов из сформированных словарей


def get_vocabulary_words():  # возвращает пару ру и ен слов для сравнения
    global sequence_number
    sequence_number += 1
    word_en = vocabulary_en[sequence_number]
    word_ru = vocabulary_ru[sequence_number]
    word_id = vocabulary_id[sequence_number]
    return word_en, word_ru, word_id


# ДЛЯ ТЕСТИРОВАНЯ ======================

def choose_(user_chose):  # выбор варианта переноса повторения слова
    if user_chose == 1:
        return change_time_output_again(w_id)
    elif user_chose == 2:
        return change_time_output_easy(w_id)
    elif user_chose == 3:
        return change_time_output_good(w_id)
    elif user_chose == 4:
        return change_time_output_hard(w_id)
    else:
        return 'ERROR input fail'


def start_train():  # запуск основной логики
    global w_id
    w_en, w_ru, w_id = get_vocabulary_words()
    print(w_id)
    while True:
        print(f'word: {w_en}')
        user_word_ru = input('input: ')
        if user_word_ru == w_ru:
            user_change_repeat = input('Yes\nchange 1-2-3-4: ')
            choose_(int(user_change_repeat))
            return 'next word'
        else:
            print('No, try again')


# cursor = con.cursor()
# cursor.execute("""SELECT *
#                FROM english_words.eng_words_new
#                ORDER BY id;""")
# rows = cursor.fetchall()
# print('\nСтатистика:')
# for row in rows:
#     print(f'"{row[0]}" - {row[1]} - {row[2]} - {row[3]}- {row[4]}')

for _ in range(counter_vocabulary()):
    start_train()
