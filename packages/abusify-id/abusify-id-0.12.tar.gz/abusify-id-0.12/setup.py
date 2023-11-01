from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='abusify-id',
    version='0.12',
    description='Abusiveness Verification in Bahasa Indonesia',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={
        'abusify_id': ['.env', 'model.pkl', 'tfidf_vectorizer.pkl'],
    },
    install_requires=[
        'scikit-learn',
        'pandas',
        'nltk',
        'pymysql',
        'python-decouple',
        'fuzzywuzzy',
        'python-Levenshtein',
    ],
)
