from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
# import util

import requests
import hashlib
import csv
import datetime 

def crawl_youju(url):
    options = webdriver.ChromeOptions()
    options.headless = False  # Change to True if you want browser to be headless
    browser = webdriver.Chrome(options=options)

    browser.get(url)

    # Get the initial scroll height of the web page
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom of the page
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for the page to load more content (you can adjust the sleep time as needed)
        time.sleep(5)

        # Calculate the new scroll height and compare with the last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If the new scroll height is equal to the last scroll height, break the loop
            # as it means we have reached the end of the page
            break
        last_height = new_height






    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    tuples = []
    divs = soup.find_all('div', class_='post-thumb')

    for div in divs:
        a_tag = div.find('a')
        if a_tag and a_tag.has_attr('href'):
            link = a_tag['href']
            browser.get(link)
            inner_html = browser.page_source
            tuples.append((link, inner_html))
            time.sleep(3)






    browser.quit()
    return tuples

# youju updates regularly. 9 posts on frontpage, if you haven't crawled in 2 weeks, you might need to scrol down to crawl more
# Have to use selenium, otherwise will get 403 access forbiddden
# 如果太烦，可以尝试发现他的ajax request url

def crawl_new_articles():
    print("Updating youju, this will take a minute. Expect a browser window to pop up")
    with open(path+'lookup_table_youju.csv', mode='r+', newline='', encoding='utf-8') as file:
        # dict for deduplication
        reader = csv.DictReader(file)
        existing_ids = {row['unique_id'] for row in reader}
        
        
        options = webdriver.ChromeOptions()
        options.headless = False  # Change to True if you want browser to be headless
        browser = webdriver.Chrome(options=options)

        browser.get(url)
        time.sleep(2)
        page_source = browser.page_source

        soup = BeautifulSoup(page_source, 'html.parser')
        divs = soup.find_all('div', class_='post-thumb')
        for div in divs:
            link = div.find('a')['href']
            unique_id = hashlib.md5(link.encode()).hexdigest()
            # add htmls that are new 
            if unique_id not in existing_ids:
                existing_ids.add(unique_id)
                browser.get(link)
                time.sleep(2)
                article_page_source = browser.page_source
                with open(path + f'htmls_youju/{unique_id}.html', 'w', encoding='utf-8') as html_file:
                    html_file.write(article_page_source)

                # Write a new line into the CSV file
                timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H:%M:%S')
                file.write(f'\n{unique_id},{link},{timestamp}')
                print("New Article: ", link)
        # else: The unique_id is already in the CSV, so we skip it


    print("Finished updating youju")

url = 'https://chinafactcheck.com/?cat=11'
path = '/Users/jimmynian/code/AMICA/crawlers/youju/'

if __name__ == '__main__':    
    None 
    # htmls = crawl_youju(url)
    # if htmls is not None:
    #     util.save_all_htmls(path+'htmls_youju', path+'lookup_table_youju', htmls)