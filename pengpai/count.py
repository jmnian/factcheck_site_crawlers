from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def count_articles(url):
    options = Options()
    options.headless = True
    browser = webdriver.Chrome(options=options)
    
    try:
        browser.get(url)
        browser.implicitly_wait(10)
        
        # Locate and click the "有定论" tab
        tab = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="有定论"]'))
        )
        tab.click()
        
        # Allow the page to load the new tab content
        time.sleep(5)  # Adjust sleep time as necessary
        
        # Initial scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")
        
        while True:
            # Simulate pressing the "End" key to scroll down
            actions = webdriver.ActionChains(browser)
            actions.send_keys(Keys.END)
            actions.perform()
            
            # Wait for a while to allow new content to load
            time.sleep(3)  # Adjust sleep time as necessary
            
            # Calculate new scroll height and compare with the last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # Exit loop when no more content is loaded
            last_height = new_height
        
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        articles = soup.find_all('div', {'data-v-4fd4e45f': True, 'data-v-753183f7': True, 'class': 'van-col van-col--8 large_item'})
        return len(articles)
    except Exception as e:
        print(f'An error occurred: {e}')
        return None
    finally:
        browser.quit()

if __name__ == '__main__':
    url = 'https://www.factpaper.cn/large'
    article_count = count_articles(url)
    if article_count is not None:
        print(f'Number of articles: {article_count}')