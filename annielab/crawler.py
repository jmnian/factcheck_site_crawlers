# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import TimeoutException
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
        # Hard code the number of clicks on "Load More" because there's only about 100 posts
        click_times = 5

        while click_times > 0:
            click_times -= 1
            # Simulate pressing the "End" key to scroll down
            actions = webdriver.ActionChains(browser)
            actions.send_keys(Keys.END)
            actions.perform()

            # Try clicking the "Load More" button
            try:
                load_more_button = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.tg-load-more a[class='tg-load-more-btn']"))
                )
                browser.execute_script("arguments[0].click();", load_more_button)
                time.sleep(5)
            except Exception as e:
                print(f"Error: {e}")
                break 
        print("break out of while loop")
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Find all h2 elements with class 'cm-entry-title'
        h2_elements = soup.find_all('h2', class_='cm-entry-title')
        
        for h2 in h2_elements:
            a_tag = h2.find('a')
            if a_tag:
                link = a_tag['href']
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
        
        
# Annie lab doesn't post frequently, so I just crawl their homepage which has 30 articles. 
# If it's been more than a year since last crawl, then just crawl the whole thing all over again using crawl_htmls(url)
def crawl_new_articles():
    with open(path+'lookup_table_annielab.csv', mode='r+', newline='', encoding='utf-8') as file:
        # dict for deduplication
        reader = csv.DictReader(file)
        existing_ids = {row['unique_id'] for row in reader}
        
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            divs = soup.find_all('div', class_='cm-featured-image')

            for div in divs:
                link = div.find('a')['href']
                unique_id = hashlib.md5(link.encode()).hexdigest()
                # add htmls that are new 
                if unique_id not in existing_ids:
                    article_response = requests.get(link)
                    if article_response.status_code == 200:
                        with open(path + f'htmls_annielab/{unique_id}.html', 'w', encoding='utf-8') as html_file:
                            html_file.write(article_response.text)

                        # Write a new line into the CSV file
                        timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H:%M:%S')
                        file.write(f'\n{unique_id},{link},{timestamp}')
                        print("New Article: ", link)
                # else: The unique_id is already in the CSV, so we skip it

        else:
            print(f"Failed to retrieve web page. Status code: {response.status_code}")
    print("Finished updating annielab")
    

url = 'https://annielab.org/category/chinese/'
path = '/Users/jimmynian/code/AMICA/crawlers/annielab/'

if __name__ == '__main__':
    None
    
    # htmls = crawl_htmls(url)
    # if htmls is not None:
    #     util.save_all_htmls(path+'htmls_annielab', path+'lookup_table_annielab.csv', htmls)