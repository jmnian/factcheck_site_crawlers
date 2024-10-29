import os
import json

def count_files_in_directory(directory):
    html_count = 0
    piyao_len = 0

    for root, dirs, files in os.walk(directory):
        if root.split('/')[-1].startswith("htmls_"):
            count = sum(1 for file in files if file.endswith('.html'))
            html_count += count
            print(f"{root.split('/')[-1]}: {count}")

        if "all_articles.json" in files:
            with open(os.path.join(root, "all_articles.json"), 'r') as json_file:
                data = json.load(json_file)
                piyao_len += len(data)

    return html_count, piyao_len

directory_path = "/Users/jimmynian/code/AMICA/crawlers"
htmls, piyao_len = count_files_in_directory(directory_path)
print(f"Total piyao.org.cn articles: {piyao_len}")
print(f"Total articles in raw html :  {htmls}")
print(f"Sum: {htmls + piyao_len}")