from setuptools import setup, find_packages

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

setup(
    name='abusify-id',
    version='0.11',
    description='Abusiveness Verification in Bahasa Indonesia',
    long_description=long_description,
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
