import re
from pathlib import Path
from time import sleep

from requests import get


def extract_info(url):
    res = get(url)
    content = res.text
    return content * int(len(content) > 1000)


if __name__ == '__main__':
    base_url = 'https://arzamas.academy/mag/arts?page='  # сайт, с которого начнет работу паук (92)
    pattern = r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"'

    page = 2
    text_urls = []
    while len(text_urls) < 500:
        data = extract_info(f"{base_url}{page}")
        print(data)
        links = re.findall(pattern, data)


        for i in links:
            if '/mag/' in i and 'page' not in i:
                text_urls.append(i[1:])
        page += 1
        sleep(0.9)

    print(len(text_urls))
    print(text_urls)

    for link in text_urls:
        if Path(f"./raw_html_files/{link.replace('/', '_')}.html").exists():
            print('skip')
            continue
        html_code = extract_info(f"https://arzamas.academy/{link}")
        with open(f"./raw_html_files/{link.replace('/', '_')}.html", 'w') as file:
            file.write(html_code)
