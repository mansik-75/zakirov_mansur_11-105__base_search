import json
import re


def shunting_yard(tokens):
    precedence = {'!': 3, '&&': 2, '||': 1}
    output = []
    operators = []

    for token in tokens:
        if token == '(':
            operators.append(token)
        elif token == ')':
            while operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()
        elif token in precedence:
            while (operators and operators[-1] != '(' and
                   precedence[operators[-1]] >= precedence[token]):
                output.append(operators.pop())
            operators.append(token)
        else:
            output.append(token)

    while operators:
        output.append(operators.pop())

    return output

def and_(a, b):
    return a & b

def or_(a, b):
    return a | b

def not_(a, all_docs):
    return all_docs - a

def boolean_search(index, query):
    tokens = re.findall(r'\(|\)|\w+|\&\&|\|\||\!', query)

    postfix = shunting_yard(tokens)

    all_docs = set()
    for doc_list in index.values():
        all_docs.update(doc_list)

    stack = []
    for token in postfix:
        if token == '&&':
            b = stack.pop()
            a = stack.pop()
            stack.append(and_(a, b))
        elif token == '||':
            b = stack.pop()
            a = stack.pop()
            stack.append(or_(a, b))
        elif token == '!':
            a = stack.pop()
            stack.append(not_(a, all_docs))
        else:
            docs = set(index.get(token, []))
            stack.append(docs)

    return sorted(stack.pop()) if stack else []


inverted_index = json.load(open('./inverted_index.json', 'r', encoding='utf8'))
req = "челове && картина && (фильм || кино)"

result = boolean_search(inverted_index, req)
print(f"Результат поиска '{req}': {result}")
