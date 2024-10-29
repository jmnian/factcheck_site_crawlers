from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
# import util
import time
import requests
import hashlib
import csv
import datetime

def crawl_mygopen(url):
    options = Options()
    options.headless = True
    browser = webdriver.Chrome(options=options)

    results = []
    page_num = 1

    while True:
        current_url = f"{url}#archive-page-{page_num}"
        browser.get(current_url)
        time.sleep(3)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all <a> tags with the specified class
        a_tags = soup.find_all('a', class_='thumbnail item-thumbnail')
        print(current_url)
        if not a_tags:  # If no such <a> tags are found, break the loop
            break

        for a_tag in a_tags:
            if a_tag.has_attr('href'):
                link = a_tag['href']
                browser.get(link)
                inner_html = browser.page_source
                results.append((link, inner_html))

        page_num += 1

    browser.quit()
    return results

# mygopen updates frquently. I go from first page and on, exit until I see a duplicate link in lookup_table_mygopen.csv

def crawl_new_articles():
    

    with open(path+'lookup_table_mygopen.csv', mode='r+', newline='', encoding='utf-8') as file:
        # dict for deduplication
        reader = csv.DictReader(file)
        existing_ids = {row['unique_id'] for row in reader}
        page_num = 1
        saw_crawled_link = False
        
        while not saw_crawled_link:
            current_url = f"{url}#archive-page-{page_num}"
            # print("current url:", current_url)
            options = Options()
            options.headless = True
            browser = webdriver.Chrome(options=options)
            browser.get(current_url)
            
            time.sleep(3)
            page_source = browser.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            a_tags = soup.find_all('a', class_='thumbnail item-thumbnail')
            for a_tag in a_tags:
                link = a_tag['href']
                unique_id = hashlib.md5(link.encode()).hexdigest()
                # add htmls that are new 
                if unique_id not in existing_ids:
                    article_response = requests.get(link)
                    if article_response.status_code == 200:
                        with open(path + f'htmls_mygopen/{unique_id}.html', 'w', encoding='utf-8') as html_file:
                            html_file.write(article_response.text)

                        # Write a new line into the CSV file
                        timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H:%M:%S')
                        file.write(f'\n{unique_id},{link},{timestamp}')
                        print("New Article: ", link)
                    else:
                        print("Got article response code:", article_response.status_code)
                else: 
                    saw_crawled_link = True
                    break
                
            page_num += 1
            browser.quit()
            
    
    print("Finished updating mygopen")

url = 'https://www.mygopen.com/search/label/%E8%AC%A0%E8%A8%80'
path = '/Users/jimmynian/code/AMICA/crawlers/mygopen/'

if __name__ == '__main__':
    None
    
    # htmls = crawl_mygopen(url)
    # if htmls is not None:
    #     util.save_all_htmls(path+'htmls_mygopen', path+'lookup_table_mygopen', htmls)

