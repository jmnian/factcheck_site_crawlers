# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import TimeoutException
# from bs4 import BeautifulSoup
# import time
# import util 
# import pickle
# import os

# def crawl_rfa(url):
#     options = Options()
#     options.headless = True
#     browser = webdriver.Chrome(options=options)

#     if not os.path.exists("crawlers/rfa/rfa_all_article_boxes.pkl"):
#         links = []
#         urls_htmls_tuples = []
        
#         i = 0
#         while True:
#             new_url = url + str(i*30)
#             browser.get(new_url)
#             browser.implicitly_wait(10) 
#             page_source = browser.page_source
#             soup = BeautifulSoup(page_source, 'html.parser')
#             divs = soup.find_all('div', class_='teaserimg')

#             # no search result, meaning we have reached the end
#             if not divs:
#                 print("no reuslt")
#                 break
            
#             for div in divs:
#                 a_tag = div.find('a')
#                 if a_tag and a_tag.has_attr('href'):
#                     link = a_tag['href']
#                     links.append(link)
#             i += 1

#         with open('crawlers/rfa/rfa_all_links.pkl', 'wb') as file:
#             pickle.dump(links, file)
#     else: 
#         with open("crawlers/rfa/rfa_all_links.pkl", "rb") as file:
#             links = pickle.load(file)
#     print(len(links))
#     print(links)

#     count = 1
#     # For each 'searchresult' div, find 'teaserimg' div's first 'a' tag and get its 'href'
#     for link in links:
#         try:
#             browser.get(link)
#         except TimeoutException:
#             print(f"Timed out while loading {link}. Moving on to the next link.")
#         inner_html = browser.page_source
#         urls_htmls_tuples.append((link, inner_html))
#         if count % 20 == 0:
#             print(count)
#         count += 1

#     browser.quit()
#     return urls_htmls_tuples
    
# if __name__ == '__main__':    
#     url = 'https://www.rfa.org/mandarin/@@search?sort_on=&sort_order=&section_name=&SearchableText=%E4%BA%8B%E5%AE%9E%E6%9F%A5%E6%A0%B8&b_start:int='
#     path = '/Users/jimmynian/code/AMICA/crawlers/rfa/'
#     htmls = crawl_rfa(url)
#     if htmls is not None:
#         util.save_all_htmls(path+'htmls_rfa', path+'lookup_table_rfa', htmls)




import requests
from bs4 import BeautifulSoup
import os
import time
# import util
import hashlib
import csv
import datetime

def crawl_rfa(base_url, interval=30):
    links = []
    urls_htmls_tuples = []
    session = requests.Session()  # Use a session for connection pooling
    
    i = 0
    while True:
        current_url = base_url + str(i * interval)
        print(f"Crawling {current_url}")
        response = session.get(current_url)
        if response.status_code != 200:
            print(f"Failed to retrieve the page: Status code {response.status_code}")
            break
        
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all('div', class_='teaserimg')

        if not divs:
            print("No result, reached the end.")
            break
        
        for div in divs:
            a_tag = div.find('a')
            if a_tag and a_tag.has_attr('href'):
                link = a_tag['href']
                links.append(link)

        if i % (interval // 30) == 0:  # Fetch articles every interval pages
            for link in links:
                print(f"Fetching {link}")
                article_response = session.get(link)
                if article_response.status_code == 200:
                    inner_html = article_response.text
                    urls_htmls_tuples.append((link, inner_html))
                time.sleep(2)  # Sleep to avoid aggressive crawling
            links = []  # Reset links after processing

        i += 1
        time.sleep(5)  # Sleep to avoid aggressive crawling
    
    return urls_htmls_tuples


# rfa updates about 10 articles per monhth. Each page has 30 articles, so I just crawl first page
# if you haven't crawled in a year, consider recrawling the whole thing

def crawl_new_articles():
    with open(path+'lookup_table_rfa.csv', mode='r+', newline='', encoding='utf-8') as file:
        # dict for deduplication
        reader = csv.DictReader(file)
        existing_ids = {row['unique_id'] for row in reader}
        
        response = requests.get(first_page_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            divs = soup.find_all('div', class_='teaserimg')
            for div in divs:
                link = div.find('a')['href']
                unique_id = hashlib.md5(link.encode()).hexdigest()
                # add htmls that are new 
                if unique_id not in existing_ids:
                    existing_ids.add(unique_id)
                    article_response = requests.get(link)
                    if article_response.status_code == 200:
                        with open(path + f'htmls_rfa/{unique_id}.html', 'w', encoding='utf-8') as html_file:
                            html_file.write(article_response.text)

                        # Write a new line into the CSV file
                        timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H:%M:%S')
                        file.write(f'\n{unique_id},{link},{timestamp}')
                        print("New Article: ", link)
            # else: The unique_id is already in the CSV, so we skip it

        else:
            print(f"Failed to retrieve web page. Status code: {response.status_code}")
    print("Finished updating rfa")

first_page_url = 'https://www.rfa.org/mandarin/@@search?sort_on=&sort_order=&section_name=&SearchableText=%E4%BA%8B%E5%AE%9E%E6%9F%A5%E6%A0%B8&b_start:int=0'
path = '/Users/jimmynian/code/AMICA/crawlers/rfa/'
base_url = 'https://www.rfa.org/mandarin/@@search?sort_on=&sort_order=&section_name=&SearchableText=%E4%BA%8B%E5%AE%9E%E6%9F%A5%E6%A0%B8&b_start:int='

if __name__ == '__main__':
    None 
    
    # htmls = crawl_rfa(base_url)
    # if htmls:
    #     util.save_all_htmls(path + 'htmls_rfa', path + 'lookup_table_rfa', htmls)
    #     print("Finished crawling and saving HTML content.")