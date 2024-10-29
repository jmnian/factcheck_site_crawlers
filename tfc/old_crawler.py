import csv
import requests
from bs4 import BeautifulSoup

def extract_article(url):
    # Fetch the HTML content of the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the text content of "h" and "p" tags
    text = ''
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
        text += tag.get_text(strip=True) + ' '

    # Write the text content to the CSV file
    csv_writer.writerow([url, text])

def main():
    url = 'https://tfc-taiwan.org.tw/articles/report?page='
    # as of 4/23/2023, their debunked articles have 232 pages, "page" ranges from 0 to 231
    visited = []
    base = 'https://tfc-taiwan.org.tw'
    for i in range(232):
        page_url = url + str(i)
        print("on page", i)
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href not in visited and href.startswith('/articles/') and len(href) == 14:
                article_url = base + href
                extract_article(article_url)
                visited.append(href)



# Initialize the CSV writer
csv_file = open('tfc_crawler/tfc_raw.csv', 'w', newline='', encoding='utf-16')
csv_writer = csv.writer(csv_file)

#run main
main()

# Close the CSV file
csv_file.close()
print("file closed")

