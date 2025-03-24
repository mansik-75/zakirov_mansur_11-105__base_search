from bs4 import BeautifulSoup
from nltk import TreebankWordTokenizer, RegexpTokenizer
from nltk.corpus import stopwords
from pymystem3 import Mystem

tokenizer = RegexpTokenizer(r'[а-яА-ЯёЁ]+')
stop_words = set(stopwords.words('russian'))
stop_words.add('х')

m = Mystem()

with open('index.txt', 'r') as index:
    for line in index.readlines():
        file_name = line.strip().split(' ')[1]
        print(file_name)
        with open(f'./raw_html_files/{file_name}', 'r') as file:
            beauty = BeautifulSoup(file.read())
            tokens = set()
            for p in beauty.find_all('p'):
                res = [word for word in tokenizer.tokenize(p.text) if word.lower() not in stop_words]
                tokens |= set(res)
                print(res)
            lemmas = dict()
            print(tokens)
            for token in tokens:
                lemma = m.lemmatize(token)[0]
                if lemma not in lemmas:
                    lemmas[lemma] = []
                lemmas[lemma].append(token)
            with open(f'./tokens/token__{file_name}', 'w') as token_file:
                token_file.writelines([f"{token}\n" for token in tokens])
            with open(f'./lemmas/lemma__{file_name}', 'w') as lemma_file:
                for key in lemmas:
                    lemma_file.write(f"{key}: {' '.join(lemmas[key])}\n")
            print(tokens)
            print(lemmas)
