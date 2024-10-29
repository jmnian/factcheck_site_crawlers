import csv
from datetime import datetime
import string
import requests
from bs4 import BeautifulSoup

def extract_article_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    urls = []
    for h in soup.findAll('li'):
        a = h.find('a')
        try:
            if 'href' in a.attrs:
                url = a.get('href')
                if "https://factcheck.hkbu.edu.hk/home/20" in url:
                    urls.append(url)
        except:
            pass
    return urls

def extract_article_content_from(urls, csv_writer):
    i = 0
    for article_url in urls:
        i += 1
        print("on article ", i)
        
        response = requests.get(article_url)
        soup = BeautifulSoup(response.content, "html.parser")

        article_wrappers = soup.find_all("div", {"class": "article-wrapper"})
        conclusions = soup.find_all("div", {"class": "conclusion"})
        references = soup.find_all("div", {"class": "reference"})
        containers = soup.find_all("div", {"class": "container"})
        result = ""
        date = ""
        title = ""
        for container in containers:
            if container is not None:
                span = container.find("span")
                p = container.find("p")
                h1 = container.find("h1")
                if span is not None and p is not None and h1 is not None and \
                len(container.find_all(["span", "p", "h1"])) == 3:
                    result = span.text.strip()
                    date_string = p.text.strip()
                    for i, c in enumerate(date_string):
                        if c.isdigit():
                            date = date_string[i:]
                            break
                    title = h1.text.strip()

        # extract text from p, span, and h1-h6 tags inside article-wrapper divs
        article_text = ""
        for wrapper in article_wrappers:
            for tag in wrapper.find_all(["p", "span", "h1", "h2", "h3", "h4", "h5", "h6"]):
                article_text += tag.get_text(strip=True) + ' '
        # extract text from p, span, and h1-h6 tags inside conclusion divs
        conclusion_text = ""
        for conclusion in conclusions:
            for tag in conclusion.find_all(["p", "span", "h1", "h2", "h3", "h4", "h5", "h6"]):
                conclusion_text += tag.get_text(strip=True) + ' '
        
        # extract hrefs from a tags inside reference divs
        reference_hrefs = []
        for reference in references:
            for a in reference.find_all("a"):
                reference_hrefs.append(a["href"])
        
        article_text = article_text.split("結論 ")[0]
        try:
            conclusion_text = conclusion_text.split("結論 ")[1].split("。 ")[1]
        except IndexError:
            print("index error for conculusion_text")
        csv_writer.writerow([article_url, result, title, date, article_text, conclusion_text, reference_hrefs])

csv_file = open('hkbu_crawler/hkbu_cn_raw.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['URL', 'Result', 'Date', 'Title', 'Article Content', 
                        'Conclusion', 'Reference'])
base_url = "https://factcheck.hkbu.edu.hk/home/fact-check/"
urls = extract_article_urls(base_url)
extract_article_content_from(urls, csv_writer)
csv_file.close()
print("file closed")

