from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def count_articles(url):
    options = Options()
    options.headless = True
    browser = webdriver.Chrome(options=options)
    
    try:
        browser.get(url)
        browser.implicitly_wait(10)
        
        while True:
            # Simulate pressing the "End" key to scroll down
            actions = webdriver.ActionChains(browser)
            actions.send_keys(Keys.END)
            actions.perform()

            # Try clicking the "Load More" button
            try:
                load_more_button = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.jeg_block_loadmore a[data-load='Load More']"))
                )
                browser.execute_script("arguments[0].click();", load_more_button)
                time.sleep(10)
            except Exception as e:
                print(f"Error: {e}")
                break 

        
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        articles = soup.find_all('article', {'class': 'jeg_post'})
        return len(articles)
    except Exception as e:
        print(f'An error occurred: {e}')
        return None
    finally:
        browser.quit()

if __name__ == '__main__':
    url = 'https://www.piyaoba.org/all-disinformation-alert/'
    article_count = count_articles(url)
    if article_count is not None:
        print(f'Number of articles: {article_count}')
