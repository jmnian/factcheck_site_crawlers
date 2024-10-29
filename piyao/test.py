import json

with open('/Users/jimmynian/code/AMICA/crawlers/piyao/first_5000_articles.json', 'r') as file:
    data = json.load(file)
    
i = 0
for line in data:
    print(line['title'], line['url'])
    if i == 10: break 
    i += 1