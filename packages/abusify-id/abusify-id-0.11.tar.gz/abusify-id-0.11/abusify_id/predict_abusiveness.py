import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer

module_dir = os.path.dirname(__file__)

model_path = os.path.join(module_dir, 'model.pkl')
vectorizer_path = os.path.join(module_dir, 'tfidf_vectorizer.pkl')

with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

with open(vectorizer_path, 'rb') as vectorizer_file:
    tfidf_vectorizer = pickle.load(vectorizer_file)

def predict_abusiveness(text, decimal_places=2):
    tfidf_text = tfidf_vectorizer.transform([text])
    abusiveness_score = model.predict_proba(tfidf_text)[0]
    abusiveness = abusiveness_score[1] * 100
    return format(abusiveness, f".{decimal_places}f") + "%"

def predict_abusiveness_file(input_file, output_file, decimal_places=2):
    with open(input_file, 'r') as file:
        kalimat_list = file.read().splitlines()

    with open(output_file, 'w') as output:
        for kalimat in kalimat_list:
            tfidf_text = tfidf_vectorizer.transform([kalimat])
            abusiveness_score = model.predict_proba(tfidf_text)[0]
            abusiveness = abusiveness_score[1] * 100  # Mengubah ke skala 0-100%
            output.write(f"{kalimat}\n")
            output.write(f"Abusiveness Level: {format(abusiveness, f'.{decimal_places}f')}%\n\n")
    print(f"The results have been saved in a file: {output_file}")