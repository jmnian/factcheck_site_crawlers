# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# import util
import time

from bs4 import BeautifulSoup
import requests
import hashlib
import csv
import datetime

def crawl_piyaoba(url):
    options = Options()
    options.headless = True
    browser = webdriver.Chrome(options=options)
    
    urls_htmls_tuples = []

    try:
        browser.get(url)
        browser.implicitly_wait(10)

        while True:
            # Try clicking the "Load More" button
            load_more_button = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.jeg_block_loadmore a"))
            )

            # Check if the button text is "Load More"
            if load_more_button.text == "LOAD MORE":
                browser.execute_script("arguments[0].click();", load_more_button)
                time.sleep(5)
            else:
                # If the button text is not "Load More", exit the loop
                break

        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        content_div = soup.find_all('div', class_='jeg_thumb')
        if not content_div:
            raise NameError("no div class=jeg_thumb")

        for div in content_div:
            a_tag = div.find('a')
            if a_tag.has_attr('href'):
                link = a_tag['href']
                browser.get(link)
                inner_html = browser.page_source
                urls_htmls_tuples.append((link, inner_html))
            # to not crawl too aggresively
            time.sleep(2)

        return urls_htmls_tuples
    
    except Exception as e:
        print(f'An error occurred: {e}')
        return None
    finally:
        browser.quit()

# piyaoba updates rarely. So I just pull up the first page to crawl

def crawl_new_articles():
    with open(path+'lookup_table_piyaoba.csv', mode='r+', newline='', encoding='utf-8') as file:
        # dict for deduplication
        reader = csv.DictReader(file)
        existing_ids = {row['unique_id'] for row in reader}
        
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            h3s = soup.find_all('h3', class_='jeg_post_title')
            for h3 in h3s:
                link = h3.find('a')['href']
                unique_id = hashlib.md5(link.encode()).hexdigest()
                # add htmls that are new 
                if unique_id not in existing_ids:
                    existing_ids.add(unique_id)
                    article_response = requests.get(link)
                    if article_response.status_code == 200:
                        with open(path + f'htmls_piyaoba/{unique_id}.html', 'w', encoding='utf-8') as html_file:
                            html_file.write(article_response.text)

                        # Write a new line into the CSV file
                        timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H:%M:%S')
                        file.write(f'\n{unique_id},{link},{timestamp}')
                        print("New Article: ", link)
                # else: The unique_id is already in the CSV, so we skip it

        else:
            print(f"Failed to retrieve web page. Status code: {response.status_code}")
    print("Finished updating piyaoba")

url = 'https://www.piyaoba.org/all-disinformation-alert/'
path = '/Users/jimmynian/code/AMICA/crawlers/piyaoba/'

if __name__ == '__main__':
    None
    
    # htmls = crawl_piyaoba(url)
    # if htmls is not None:
    #     util.save_all_htmls(path+'htmls_piyaoba', path+'lookup_table_piyaoba', htmls)