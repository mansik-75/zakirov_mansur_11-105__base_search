import os

if __name__ == '__main__':
    files = os.listdir('./raw_html_files')
    with open('index.txt', 'w') as file:
        count = 1
        for i in files:
            file.write(f"{count}. {i}\n")
            count += 1
