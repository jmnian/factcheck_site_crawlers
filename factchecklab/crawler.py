# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# import util 

from bs4 import BeautifulSoup
import time
import requests
import hashlib
import csv
import datetime

def crawl_htmls(url):
    options = Options()
    options.headless = True
    browser = webdriver.Chrome(options=options)

    urls_htmls_tuples = []
    
    try:
        browser.get(url)
        browser.implicitly_wait(10)

        # Initial scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")
        
        while True:
            # Simulate pressing the "End" key to scroll down
            actions = webdriver.ActionChains(browser)
            actions.send_keys(Keys.END)
            actions.perform()
            
            # Wait for a while to allow new content to load
            time.sleep(5)  # Adjust sleep time as necessary
            
            # Calculate new scroll height and compare with the last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # Exit loop when no more content is loaded
            last_height = new_height
        
        print("break out of while loop")
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        articles = soup.find_all('article', {'class': 'post-card'})
        
        for article in articles:
            a_tag = article.find('a')
            if a_tag:
                link = url+a_tag['href']
                
                # Navigate to the URL and fetch the full HTML
                browser.get(link)
                inner_html = browser.page_source
                urls_htmls_tuples.append((link, inner_html))

        return urls_htmls_tuples
    except Exception as e:
        print(f'An error occurred: {e}')
        return None
    finally:
        browser.quit()

# Factcheck Lab doesn't post frequently, so I just crawl their homepage which has 25 articles. 
# If it's been more than a year since last crawl, then just crawl the whole thing all over again using crawl_htmls(url)
def crawl_new_articles():
    with open(path+'lookup_table_factchecklab.csv', mode='r+', newline='', encoding='utf-8') as file:
        # dict for deduplication
        reader = csv.DictReader(file)
        existing_ids = {row['unique_id'] for row in reader}
        
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('article', {'class': 'post-card'})

            for article in articles:
                link = url+article.find('a')['href']
                unique_id = hashlib.md5(link.encode()).hexdigest()
                # add htmls that are new 
                if unique_id not in existing_ids:
                    article_response = requests.get(link)
                    if article_response.status_code == 200:
                        with open(path + f'htmls_factchecklab/{unique_id}.html', 'w', encoding='utf-8') as html_file:
                            html_file.write(article_response.text)

                        # Write a new line into the CSV file
                        timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H:%M:%S')
                        file.write(f'\n{unique_id},{link},{timestamp}')
                        print("New Article: ", link)
                # else: The unique_id is already in the CSV, so we skip it

        else:
            print(f"Failed to retrieve web page. Status code: {response.status_code}")
    print("Finished updating factchecklab")

url = 'https://www.factchecklab.org/'
path = '/Users/jimmynian/code/AMICA/crawlers/factchecklab/'

if __name__ == '__main__':    
    None
    
    # htmls = crawl_htmls(url)
    # if htmls is not None:
    #     util.save_all_htmls(path+'htmls_factchecklab', path+'lookup_table_factchecklab.csv', htmls)