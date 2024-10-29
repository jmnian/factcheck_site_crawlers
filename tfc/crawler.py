import time
import re
import random
import requests
from bs4 import BeautifulSoup
# import util
import pickle
import hashlib
import csv
import datetime

def crawl_tfc(base_url):
    results = []
    page_num = 0
    session = requests.Session()  # Use a session object for connection pooling
    seen_articles = set()

    while True:
        current_url = f"{base_url}articles/report?page={page_num}"
        print(f"Crawling page {page_num}...")
        response = session.get(current_url)
        if response.status_code != 200:
            print(f"Failed to retrieve page {page_num}: Status code {response.status_code}")
            break

        if page_num >= 268:
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', class_='view-content')
        if not content_div:
            print("No more content found, stopping crawl.")
            break

        a_tags = content_div.find_all('a', href=True)
        if not a_tags:  # If no such <a> tags are found, break the loop
            print("No links found, stopping crawl.")
            break

        for a_tag in a_tags:
            href = a_tag['href']
            if '/articles/' in href:
                # Extract the article number and check for duplication
                article_num = re.findall(r'/articles/(\d+)', href)
                if article_num and article_num[0] not in seen_articles:
                    seen_articles.add(article_num[0])  # Mark as seen
                    link = 'https://tfc-taiwan.org.tw' + href
                    print(f"Fetching details from {link}")
                    inner_response = session.get(link)
                    if inner_response.status_code == 200:
                        inner_html = inner_response.text
                        results.append((link, inner_html))
                    else:
                        print(f"Failed to fetch details from {link}: Status code {inner_response.status_code}")
                    # Sleep to avoid aggressive crawling
                    time.sleep(random.randint(1, 10))
            if page_num != 0 and page_num % 50 == 0:
                with open(f"/Users/jimmynian/code/AMICA/crawlers/taiwan_fact_check/{page_num}_page_results.pkl", 'wb') as pkl_file:
                    pickle.dump(results, pkl_file)
        page_num += 1
        # Add a delay to not overload the server
        time.sleep(random.randint(1, 10))

    return results

# Taiwan Fact Check updates regularly. But the code pulls all of their posts, so we're good

def crawl_new_articles():
    seen_articles = set()
    
    with open(path+'lookup_table_tfc.csv', mode='r+', newline='', encoding='utf-8') as file:
        # dict for deduplication
        reader = csv.DictReader(file)
        existing_ids = {row['unique_id'] for row in reader}
        
        page_num = 0
        session = requests.Session()  # Use a session object for connection pooling

        saw_crawled_link = False
        while not saw_crawled_link:
            current_url = f"{base_url}articles/report?page={page_num}"
            response = session.get(current_url)
            if response.status_code != 200:
                print(f"Failed to retrieve page {page_num}: Status code {response.status_code}")
                break

            if page_num >= 268:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            content_div = soup.find('div', class_='view-content')
            if not content_div:
                print("No more content found, stopping crawl.")
                break

            a_tags = content_div.find_all('a', href=True)
            if not a_tags:  # If no such <a> tags are found, break the loop
                print("No links found, stopping crawl.")
                break

            for a_tag in a_tags:
                href = a_tag['href']
                if '/articles/' in href:
                    # Extract the article number and check for duplication
                    article_num = re.findall(r'/articles/(\d+)', href)
                    if article_num and article_num[0] not in seen_articles:
                        seen_articles.add(article_num[0])  # Mark as seen
                        link = 'https://tfc-taiwan.org.tw' + href
                        unique_id = hashlib.md5(link.encode()).hexdigest()
                        # add htmls that are new 
                        if unique_id not in existing_ids:
                            article_response = session.get(link)
                            if article_response.status_code == 200:
                                with open(path + f'htmls_tfc/{unique_id}.html', 'w', encoding='utf-8') as html_file:
                                    html_file.write(article_response.text)

                                # Write a new line into the CSV file
                                timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H:%M:%S')
                                file.write(f'\n{unique_id},{link},{timestamp}')
                                print("New Article: ", link)
                            else:
                                print(f"Failed to fetch details from {link}: Status code {article_response.status_code}")
                            # Sleep to avoid aggressive crawling
                            time.sleep(2)
                        else: # saw duplicate, meaning all new articles are crawled
                            saw_crawled_link = True
                            break
            page_num += 1
            # Add a delay to not overload the server
            time.sleep(random.randint(1, 5))
    print("Finished updating tfc")

base_url = 'https://tfc-taiwan.org.tw/'
path = '/Users/jimmynian/code/AMICA/crawlers/tfc/'

if __name__ == '__main__':
    None 
    
    # base_url = 'https://tfc-taiwan.org.tw/'
    
    # htmls = crawl_tfc(base_url)
    # if htmls:
    #     util.save_all_htmls(path + 'htmls_tfc', path + 'lookup_table_tfc', htmls)
    #     print("Finished crawling and saving HTML content.")
