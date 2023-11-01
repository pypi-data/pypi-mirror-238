from decouple import config
import pymysql
import re
from fuzzywuzzy import fuzz

def create_connection():
    connection = pymysql.connect(
        host=config('DB_HOST'),
        user=config('DB_USER'),
        password=config('DB_PASSWORD'),
        db=config('DB_NAME'),
    )
    return connection

def clean_abusive_words(connection, input_text):
    words = re.findall(r'\b\w+\b|[.,\/#?!$%\^&\*;:{}=\-_`~()&+]|[-\d]+', input_text)
    clean_text = ''

    with connection.cursor() as cursor:
        for word in words:
            if word.isalnum():  
                cursor.execute("SELECT kata, versi_halus FROM kata_kasar")
                results = cursor.fetchall()

                matching_words = {}
                for kata_kasar, versi_halus in results:
                    similarity = fuzz.ratio(word.lower(), kata_kasar.lower())
                    if similarity >= 80:  
                        matching_words[kata_kasar] = (similarity, versi_halus)

                if matching_words:
                    max_similarity_word = max(matching_words, key=lambda x: matching_words[x][0])
                    kata_halus = matching_words[max_similarity_word][1]
                    if word.istitle():
                        kata_halus = kata_halus.capitalize()
                    clean_text += ' ' + kata_halus
                else:
                    clean_text += ' ' + word
            else:
                clean_text += word

    clean_text = clean_text.strip()
    clean_text = re.sub(r'\s+', ' ', clean_text)

    # Ganti semua tanda hubung dengan spasi di antara kata-kata
    clean_text = re.sub(r'\s*-\s*', ' - ', clean_text)

    return clean_text

def abusiveword_filter(input_text):
    connection = create_connection()

    try:
        cleaned_text = clean_abusive_words(connection, input_text)
        return cleaned_text
    finally:
        connection.close()