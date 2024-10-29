import requests
import json 
import time 

base_url = 'https://so.news.cn/xhtvapp/rumourSearch'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}
file_path = '/Users/jimmynian/code/AMICA/crawlers/piyao/all_articles.json'


def crawl_all():
    all_articles = []

    for page_num in range(1, 2029):
        print("on page", page_num)
        params = {
            'title': '',
            'pageNum': page_num,
            'timeInterval': '',
            'startTime': '',
            'endTime': '',
            'typeName': '',
            'pageSize': 10,
            'sort': -2,
            'callback': '?'
        }

        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()

            # Extract the 'resultList' from the 'content' attribute
            results = data.get('content', {}).get('resultList', [])

            # Extend the all_results list with the current page's results
            all_articles.extend(results)
        else:
            print("Failed to retrieve data:", response.status_code)
        
        if len(all_articles) % 100 == 0:
            print("got", len(all_articles), "articles")
        if len(all_articles) % 5000 == 0:
            file_path = f'/Users/jimmynian/code/AMICA/crawlers/piyao/first_{len(all_articles)}_articles.json'
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(all_articles, file)
        
        time.sleep(10)


    
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(all_articles, file)

    len(all_articles), file_path

def crawl_new_articles():
    def read_json_file(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    
    existing_data = read_json_file(file_path)
    existing_urls = set(item["platUniqueId"] for item in existing_data)
    merged_data = existing_data.copy()
    
    page_num = 2
    no_duplicate_seen = True 
    
    while no_duplicate_seen:
        # print("on page", page_num)
        params = {
            'title': '',
            'pageNum': page_num,
            'timeInterval': '',
            'startTime': '',
            'endTime': '',
            'typeName': '',
            'pageSize': 10,
            'sort': -2,
            'callback': '?'
        }

        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            new_data = data.get('content', {}).get('resultList', [])
            duplicate_on_this_page = 0
            for item in new_data:
                if item["platUniqueId"] not in existing_urls:
                    merged_data.append(item)
                    print("New Article: ", item['url'])
                else:
                    duplicate_on_this_page += 1
        
            if duplicate_on_this_page == len(new_data):
                # print(duplicate_on_this_page)
                no_duplicate_seen = False
        
        else:
            print("Failed to retrieve data:", response.status_code)
            
        page_num += 1
    
    with open(file_path, 'w') as file:
        json.dump(merged_data, file, indent=4)
        
    print("Finished updating piyao.org.cn")