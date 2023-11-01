from decouple import config
import pymysql
from fuzzywuzzy import fuzz

def create_connection():
    connection = pymysql.connect(
        host=config('DB_HOST'),
        user=config('DB_USER'),
        password=config('DB_PASSWORD'),
        db=config('DB_NAME'),
    )
    return connection

def find_abusive_words(connection, text):
    text = text.lower()
    words = text.split()
    abusive_words = {}

    with connection.cursor() as cursor:
        for word in words:
            cursor.execute("SELECT id, kata FROM kata_kasar WHERE %s LIKE CONCAT('%%', kata, '%%')", (word,))
            results = cursor.fetchall()
            if results:
                for result in results:
                    abusive_words[result[1]] = f"[{result[1]}](https://stopucapkasar.com/detail.php?id={result[0]})"
            else:
                similar_words = get_similar_words(word, cursor)
                if similar_words:
                    max_similarity_word = max(similar_words, key=lambda x: similar_words[x])
                    abusive_words[max_similarity_word] = similar_words[max_similarity_word]

    return abusive_words

def get_similar_words(word, cursor):
    cursor.execute("SELECT id, kata FROM kata_kasar")
    all_words = cursor.fetchall()
    similar_words = {}
    threshold = 80

    for db_id, db_word in all_words:
        similarity_score = fuzz.ratio(word, db_word.lower())
        if similarity_score >= threshold:
            similar_words[db_word] = f"[{db_word}](https://stopucapkasar.com/detail.php?id={db_id})"

    return similar_words

def abusiveword_detector(input_text):
    connection = create_connection()

    try:
        abusive_words = find_abusive_words(connection, input_text)
        if abusive_words:
            result = ', '.join(abusive_words.values())
        else:
            result = "Nothing found!"
    finally:
        connection.close()

    return result