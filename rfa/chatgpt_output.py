import os
import csv
import hashlib
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Moved save_html outside of save_all_htmls for reusability
def save_html(writer, SAVE_DIR, url, html_content):
    unique_id = hashlib.md5(url.encode()).hexdigest()
    with open(os.path.join(SAVE_DIR, f"{unique_id}.html"), "w", encoding="utf-8") as file:
        file.write(html_content)
    current_datetime = datetime.now()
    datetime_str = current_datetime.strftime('%Y_%m_%d_%H:%M:%S')
    writer.writerow({'unique_id': unique_id, 'url': url, 'crawl_date': datetime_str})

def save_all_htmls(SAVE_DIR, METADATA_FILE, html_tuples):
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    with open(METADATA_FILE, 'a', newline='') as csvfile:
        fieldnames = ['unique_id', 'url', 'crawl_date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for url, html in html_tuples:
            save_html(writer, SAVE_DIR, url, html)

def init_browser():
    options = Options()
    options.headless = True
    return webdriver.Chrome(options=options)

def crawl_rfa(browser, url):
    urls_htmls_tuples = []
    i = 0
    count = 1
    while True:
        try:
            browser.get(url + str(i*30))
            browser.implicitly_wait(3)
            page_source = browser.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            search_results = soup.find_all('div', class_='searchresult')
            if not search_results:
                break
            for result in search_results:
                teaser_img_div = result.find('div', class_='teaserimg')
                if teaser_img_div:
                    a_tag = teaser_img_div.find('a')
                    if a_tag and a_tag.has_attr('href'):
                        link = a_tag['href']
                        browser.get(link)
                        inner_html = browser.page_source
                        urls_htmls_tuples.append((link, inner_html))
                        print(count)
                        count += 1
            i += 1
        except Exception as e:
            print(f'An error occurred: {e}')
            return None
    return urls_htmls_tuples

if __name__ == '__main__':    
    url = 'https://www.rfa.org/mandarin/@@search?sort_on=&sort_order=&section_name=&SearchableText=%E4%BA%8B%E5%AE%9E%E6%9F%A5%E6%A0%B8&b_start:int='
    path = '/Users/jimmynian/code/AMICA/crawlers/rfa/'
    browser = init_browser()  # Initialize browser
    htmls = crawl_rfa(browser, url)
    browser.quit()  # Quit browser
    if htmls is not None:
        save_all_htmls(os.path.join(path, 'htmls_rfa'), os.path.join(path, 'lookup_table_rfa'), htmls)