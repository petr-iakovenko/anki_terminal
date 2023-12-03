import psycopg2
import random


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

    cur.execute("""SELECT id
                    FROM english_words.eng_words_new
                    WHERE time_request <= now() OR time_request IS NULL 
                    ORDER BY id"""
    )
    rows_ = cur.fetchall()
    key_ru = 0
    for i in rows_:
        key_ru += 1
        vocabulary_id[key_ru] = i[0]
    return vocabulary_en, vocabulary_ru, vocabulary_id  # получаю 3 словаря чтобы=


# НАЧАЛО ================== выбираем временной перенос вызова слова

def change_time_output_known(a):  # временной перенос вызова слова
    cur = con.cursor()
    cur.execute("""UPDATE english_words.eng_words_new  
                    SET time_request = CURRENT_TIMESTAMP + interval '10 day'
                    WHERE id = %s""", (int(a),))


def change_time_output_easy(a):
    cur = con.cursor()
    cur.execute("""UPDATE english_words.eng_words_new  
                    SET time_request = CURRENT_TIMESTAMP + interval '3 day'
                    WHERE id = %s""", (int(a),))


def change_time_output_good(a):
    cur = con.cursor()
    cur.execute("""UPDATE english_words.eng_words_new  
                    SET time_request = CURRENT_TIMESTAMP + interval '1 day'
                    WHERE id = %s""", (int(a),))


def change_time_output_hard(a):
    cur = con.cursor()
    cur.execute("""UPDATE english_words.eng_words_new  
                    SET time_request = CURRENT_TIMESTAMP + interval '10 minute'
                    WHERE id = %s""", (int(a),))


def change_time_output_unknown(a):
    cur = con.cursor()
    cur.execute("""UPDATE english_words.eng_words_new  
                    SET time_request = CURRENT_TIMESTAMP
                    WHERE id = %s""", (int(a),))


# КОНЕЦ ================== выбираем временной перенос вызова слова


w_id = 0
counter = 1


def get_vocabulary_words():  # возвращает рандомные пару ру и ен слов и счетчик для сравнения
    vocabulary_en, vocabulary_ru, vocabulary_id = get_vocabulary()
    sequence_number = random.randint(1, len(vocabulary_id))
    word_en = vocabulary_en[sequence_number]
    word_ru = vocabulary_ru[sequence_number]
    word_id = vocabulary_id[sequence_number]
    counter_word = len(vocabulary_id)
    return word_en, word_ru, word_id, counter_word


def choose_():  # выбор варианта переноса повторения слова
    while True:
        user_change_repeat = input('please input number between 1 and 5: ')
        if user_change_repeat == '1':
            return change_time_output_unknown(w_id)
        elif user_change_repeat == '2':
            return change_time_output_hard(w_id)
        elif user_change_repeat == '3':
            return change_time_output_good(w_id)
        elif user_change_repeat == '4':
            return change_time_output_easy(w_id)
        elif user_change_repeat == '5':
            return change_time_output_known(w_id)
        else:
            print('ERROR!')


def info_about_choose_():  # справка
    return 'Input number between 1 and 5\n' \
           'choose repeat timer:\n' \
           '1 - repeat again\n' \
           '2 - repeat in 10 minutes\n' \
           '3 - repeat in 1 day\n' \
           '4 - repeat in 3 days\n' \
           '5 - repeat in 10 days\n'


def start_train():  # запуск основной логики
    global w_id
    global counter
    while True:
        w_en, w_ru, w_id, counter = get_vocabulary_words()
        print(f'Translate word: '
              f'{w_en}')
        user_word_ru = input('Input: ')
        if user_word_ru == w_ru:
            print(f"You're right!\n"
                  f"{info_about_choose_()}")  # возвращает пару ру и ен слов для сравнения
            choose_()  # выбор варианта переноса повторения слова
        else:
            print('No, try again')

try:
    for _ in range(counter):
        start_train()
except Exception as exep:
    print(f'You have 0 unknown words. Take a break {exep}')


# def _get_all_word():
#     cursor = con.cursor()
#     cursor.execute("""SELECT *
#                    FROM english_words.eng_words_new
#                    ORDER BY id;""")
#     rows = cursor.fetchall()
#     print('\nСтатистика:')
#     for row in rows:
#         print(f'"{row[0]}" - {row[1]} - {row[2]} - {row[3]}- {row[4]}')