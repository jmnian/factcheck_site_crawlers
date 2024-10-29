# Peng Pai is a little different, it doesn't have hrefs to articles on their homepage html. 


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
# import util
import time
import pickle
import hashlib
import csv
import datetime

def scroll_to_bottom(browser):
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom of the page
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for the page to load more content (you can adjust the sleep time as needed)
        time.sleep(8)

        # Calculate the new scroll height and compare with the last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If the new scroll height is equal to the last scroll height, break the loop
            # as it means we have reached the end of the page
            break
        last_height = new_height

def click_and_save_htmls(url, tab_name, urls_htmls_tuples):
    options = webdriver.ChromeOptions()
    options.headless = False
    browser = webdriver.Chrome(options=options)
    browser.get(url)  

    tab = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//span[text()="{tab_name}"]'))
    )
    tab.click()
    
    visited_titles = set()  # Set to store visited titles to prevent duplicates

    while True:
        # Wait for div elements to be present on the page
        wait = WebDriverWait(browser, 10)
        div_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.van-col.van-col--8.large_item')))
        starting_num_elements = len(div_elements)
        
        for div in div_elements:
            # Find the unique title within the div
            title_element = div.find_element(By.CSS_SELECTOR, ".large_item_title.van-multi-ellipsis--l2")
            title_text = title_element.text.strip()
            if title_text in visited_titles:
                continue  # Skip this div as its content has already been collected
            visited_titles.add(title_text)  # Mark this title as visited

            try:
                # Scroll into view and click the div
                browser.execute_script("arguments[0].scrollIntoView();", div)
                div.click()

                # Wait for the new page to load
                wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                time.sleep(2)  # Adjust timing as necessary

                # Save the current URL and page source
                current_url = browser.current_url
                current_html = browser.page_source
                urls_htmls_tuples.append((current_url, current_html))

                if len(urls_htmls_tuples) % 10 == 0:
                    print("*************************")
                    print(len(urls_htmls_tuples))

                # Navigate back to the main page to continue with the next div
                browser.back()
                wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                time.sleep(2)  # Adjust timing as necessary
            except WebDriverException as e:
                print(f"An error occurred: {e}")

        # Scroll down to load more content
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(30)  # Wait 30 seconds for new content to load

        # Check if new elements have been loaded
        new_div_elements = browser.find_elements(By.CSS_SELECTOR, '.van-col.van-col--8.large_item')
        if len(new_div_elements) <= starting_num_elements:
            break  # No new elements were loaded, we are at the bottom
    browser.quit()
    return urls_htmls_tuples


# Pengpai updates occationally. You can adjust the number of times to scroll and the code will gather all the articles

def crawl_new_articles():
    print("Updating pengpai, this will take a minute. Expect a browser window to pop up")
    print("Also expect a error element not interactable. But don't worry about it.")
    print()
    
    with open(path+'lookup_table_pengpai.csv', mode='r+', newline='', encoding='utf-8') as file:
        # dict for deduplication
        reader = csv.DictReader(file)
        existing_ids = {row['unique_id'] for row in reader}
        
        options = webdriver.ChromeOptions()
        options.headless = False
        browser = webdriver.Chrome(options=options)
        browser.get(url)  

        tab = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//span[text()="有定论"]'))
        )
        tab.click()
        
        visited_titles = set()  # Set to store visited titles to prevent duplicates


        # Wait for div elements to be present on the page
        wait = WebDriverWait(browser, 10)
        div_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.van-col.van-col--8.large_item')))
        
        for div in div_elements:
            # Find the unique title within the div
            title_element = div.find_element(By.CSS_SELECTOR, ".large_item_title.van-multi-ellipsis--l2")
            title_text = title_element.text.strip()
            if title_text in visited_titles:
                continue  # Skip this div as its content has already been collected
            visited_titles.add(title_text)  # Mark this title as visited

            try:
                # Scroll into view and click the div
                browser.execute_script("arguments[0].scrollIntoView();", div)
                div.click()

                # Wait for the new page to load
                wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                time.sleep(2)  # Adjust timing as necessary

                # Save the current URL and page source
                link = browser.current_url
                current_html = browser.page_source
                
                unique_id = hashlib.md5(link.encode()).hexdigest()
                # add htmls that are new 
                if unique_id not in existing_ids:
                    existing_ids.add(unique_id)
                    with open(path + f'htmls_pengpai/{unique_id}.html', 'w', encoding='utf-8') as html_file:
                        html_file.write(current_html)

                    # Write a new line into the CSV file
                    timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H:%M:%S')
                    file.write(f'\n{unique_id},{link},{timestamp}')
                    print("New Article: ", link)

                # Navigate back to the main page to continue with the next div
                browser.back()
                wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                time.sleep(2)  # Adjust timing as necessary
            except WebDriverException as e:
                print(f"An error occurred: {e}")

    browser.quit()
    print("Finished updating pengpai")

url = "https://www.factpaper.cn/large"
path = '/Users/jimmynian/code/AMICA/crawlers/pengpai/'

def crawl_all():
    htmls = []
    htmls = click_and_save_htmls(url, "有定论", htmls)
    htmls = click_and_save_htmls(url, "核查中", htmls)

    if len(htmls) > 1:
        util.save_all_htmls(path+'htmls_pengpai', path+'lookup_table_pengpai', htmls)
    
        

if __name__ == "__main__":
    None 
    # crawl_all()
    