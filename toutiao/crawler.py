from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
# import util 
import pickle
import os

import hashlib
import csv
import datetime

def crawl_toutiao(url):

    options = webdriver.ChromeOptions()
    options.headless = False  # Change to True if you want browser to be headless
    browser = webdriver.Chrome(options=options)

    if not os.path.exists("crawlers/toutiao/toutiao_full_pagesource.pkl"):
    #Scroll to the bottom
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

    #Save the current full page in case something breaks
        page_source = browser.page_source
        with open('toutiao_full_pagesource.pkl', 'wb') as file:
            pickle.dump(page_source, file)

    else:
        with open("crawlers/toutiao/toutiao_full_pagesource.pkl", "rb") as file:
            page_source = pickle.load(file)
#Pick out all the urls
    soup = BeautifulSoup(page_source, 'html.parser')
    tuples = []
    divs = soup.find_all('div', class_='feed-card-article-l')
    print("Number of articles in toutiao piyao: ", len(divs))

    count = 0
    for div in divs:
        a_tag = div.find('a')
        if a_tag and a_tag.has_attr('href'):
            link = a_tag['href']
            browser.get(link)
            inner_html = browser.page_source
            tuples.append((link, inner_html))
            time.sleep(3)
            count += 1
        if count % 20 == 0:
            print(count)

    browser.quit()
    return tuples

# toutiao updates frequently. About 30 articles on homepage, and on average 1 post per day. 

def crawl_new_articles():
    print("Updating toutiao, this will take few minutes. Expect a browser window to pop up")
    with open(path+'lookup_table_toutiao.csv', mode='r+', newline='', encoding='utf-8') as file:
        # dict for deduplication
        reader = csv.DictReader(file)
        existing_ids = {row['unique_id'] for row in reader}
        
        options = Options()
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        browser = webdriver.Chrome(options=options)
        browser.get(url)
        time.sleep(10)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        divs = soup.find_all('div', class_='feed-card-article-l')
        for div in divs:
            link = div.find('a')['href']
            unique_id = hashlib.md5(link.encode()).hexdigest()
            # add htmls that are new 
            if unique_id not in existing_ids:
                existing_ids.add(unique_id)
                browser.get(link)
                article_page_source = browser.page_source
                with open(path + f'htmls_toutiao/{unique_id}.html', 'w', encoding='utf-8') as html_file:
                    html_file.write(article_page_source)

                # Write a new line into the CSV file
                timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H:%M:%S')
                file.write(f'\n{unique_id},{link},{timestamp}')
                print("New Article: ", link)
        # else: The unique_id is already in the CSV, so we skip it
        
    print("Finished updating toutiao")


url = 'https://www.toutiao.com/c/user/token/MS4wLjABAAAAC6iKyx7z-k1NhYbBohkLPYdPcJTXQlD2Z-bm2sE9u_U/?source=profile'
path = '/Users/jimmynian/code/AMICA/crawlers/toutiao/'

if __name__ == '__main__':    
    None 

    # htmls = crawl_toutiao(url)
    # if htmls is not None:
    #     util.save_all_htmls(path+'htmls_toutiao', path+'lookup_table_toutiao', htmls)