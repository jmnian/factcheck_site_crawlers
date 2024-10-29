# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# import util

from bs4 import BeautifulSoup
import requests
import hashlib
import csv
import datetime

def crawl_htmls(url):
    options = Options()
    options.headless = True
    browser = webdriver.Chrome(options=options)

    browser.get(url)
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all <li> items
    li_items = soup.find_all('li')

    results = []

    for li in li_items:
        # For each <li>, find the first div with class "card mb-2"
        card_div = li.find('div', class_='card mb-2')
        if card_div:
            a_tag = card_div.find('a')
            if a_tag and a_tag.has_attr('href'):
                link = a_tag['href']
                browser.get(link)
                inner_html = browser.page_source
                results.append((link, inner_html))

    browser.quit()
    return results

# hkbu update regularly. But the code pulls all of their posts, so we're good
# If it's been more than a year since last crawl, then just crawl the whole thing all over again using crawl_htmls(url)
def crawl_new_articles():
    with open(path+'lookup_table_hkbu.csv', mode='r+', newline='', encoding='utf-8') as file:
        # dict for deduplication
        reader = csv.DictReader(file)
        existing_ids = {row['unique_id'] for row in reader}
        
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            li_items = soup.find_all('li')
            for li in li_items:
                card_div = li.find('div', class_='card mb-2')
                if card_div:
                    link = card_div.find('a')['href']
                    
                    unique_id = hashlib.md5(link.encode()).hexdigest()
                    # add htmls that are new 
                    if unique_id not in existing_ids:
                        article_response = requests.get(link)
                        if article_response.status_code == 200:
                            with open(path + f'htmls_hkbu/{unique_id}.html', 'w', encoding='utf-8') as html_file:
                                html_file.write(article_response.text)

                            # Write a new line into the CSV file
                            timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H:%M:%S')
                            file.write(f'\n{unique_id},{link},{timestamp}')
                            print("New Article: ", link)
                # else: The unique_id is already in the CSV, so we skip it

        else:
            print(f"Failed to retrieve web page. Status code: {response.status_code}")
    print("Finished updating hkbu")

url = 'https://factcheck.hkbu.edu.hk/home/fact-check/'
path = '/Users/jimmynian/code/AMICA/crawlers/hkbu/'

if __name__ == '__main__':
    None 
    
    # htmls = crawl_htmls(url)
    # if htmls is not None:
    #     util.save_all_htmls(path+'htmls_hkbu', path+'lookup_table_hkbu', htmls)