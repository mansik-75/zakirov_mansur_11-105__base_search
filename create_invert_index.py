import json
import os

invert_dict = dict()
start_dir = './tokens'

for filename in os.listdir(start_dir):
    path = os.path.join(start_dir, filename)
    with open(path, 'r') as f:
        tokens = f.readlines()
        for token in tokens:
            token = token.strip()
            if token not in invert_dict:
                invert_dict[token] = []
            if filename not in invert_dict[token]:
                invert_dict[token].append(filename)

print(invert_dict)
json.dump(invert_dict, open('inverted_index.json', 'w', encoding='utf8'))
