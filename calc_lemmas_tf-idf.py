import os
import math


def calculate_tf(documents):
    tf = {}

    for doc_id, terms in documents.items():
        total_terms = list()
        for term in terms:
            total_terms.append(documents[doc_id][term])
        term_counts = dict()

        for term in terms:
            term_counts[term] = term_counts.get(term, 0) + len(documents[doc_id][term])

        tf[doc_id] = {term: count / len(total_terms) for term, count in term_counts.items()}

    return tf


def calculate_idf(documents):
    idf = {}
    total_documents = len(documents)

    doc_frequency = {}

    for terms in documents.values():
        for term in terms:
            doc_frequency[term] = doc_frequency.get(term, 0) + len(terms[term])

    for term, count in doc_frequency.items():
        idf[term] = math.log(total_documents / count)

    return idf


def load_documents_from_folder(folder_path):
    documents = {}

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        documents[filename] = dict()
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    lemma, forms = line.strip().split(': ')
                    documents[filename][lemma] = list(elem for elem in forms.split())

    return documents


if __name__ == "__main__":
    documents = load_documents_from_folder('lemmas')

    tf = calculate_tf(documents)
    idf = calculate_idf(documents)

    for file in tf:
        with open(f'./lemmas_tf-idf/{file}', 'w') as f:
            for term in tf[file]:
                f.write(f'{term} {idf[term]} {tf[file][term] * idf[term]}\n')
