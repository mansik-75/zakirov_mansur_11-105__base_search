import os
import math


def calculate_tf(documents):
    tf = {}

    for doc_id, terms in documents.items():
        total_terms = len(terms)
        term_counts = dict()

        for term in terms:
            term_counts[term] = term_counts.get(term, 0) + 1

        tf[doc_id] = {term: count / total_terms for term, count in term_counts.items()}

    return tf


def calculate_idf(documents):
    idf = {}
    total_documents = len(documents)

    doc_frequency = {}

    for terms in documents.values():
        unique_terms = set(terms)
        for term in unique_terms:
            doc_frequency[term] = doc_frequency.get(term, 0) + 1

    for term, count in doc_frequency.items():
        idf[term] = math.log(total_documents / count)

    return idf


def load_documents_from_folder(folder_path):
    documents = {}

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                terms = f.read().split()
                documents[filename] = terms

    return documents


if __name__ == "__main__":
    documents = load_documents_from_folder('tokens')

    tf = calculate_tf(documents)
    idf = calculate_idf(documents)

    for file in tf:
        with open(f'./tokens_tf-idf/{file}', 'w') as f:
            for term in tf[file]:
                f.write(f'{term} {idf[term]} {tf[file][term] * idf[term]}\n')
