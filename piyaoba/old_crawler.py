import csv
import requests
from bs4 import BeautifulSoup

# Set the URL of the homepage
url = 'http://www.piyaoba.org/'

# Initialize the CSV writer
csv_file = open('piyaoba.csv', 'w', newline='', encoding='utf-16')
csv_writer = csv.writer(csv_file)
visited = []

# Function to extract text content and follow links recursively
def extract_content(url):
    # Fetch the HTML content of the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the text content of "h" and "p" tags
    text = ''
    
    
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
        text += tag.get_text(strip=True) + ' '
    date_tag = soup.find('span', {'class': 'elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-date'})
    if date_tag: 
        text += date_tag.get_text(strip=True)
    # Write the text content to the CSV file
    if text.startswith("【"):
        csv_writer.writerow([url, text])

    #Follow all the links on the page
    for link in soup.find_all('a'):
        next_url = link.get('href')
        if next_url == None:
            continue
        if 'www.piyaoba.org/' in next_url and next_url not in visited:
            visited.append(next_url)
            extract_content(next_url)

# Call the function to start the extraction process
extract_content(url)

# Close the CSV file
csv_file.close()
print("file closed")