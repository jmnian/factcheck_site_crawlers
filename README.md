# HTML Crawlers for 11 Chinese fact-check websites
As of 5/13/2024, all 11 crawlers are functioning correctly. <br>
List of sites: [Annie Lab, Factcheck Lab, HKBU Fact Check, MyGoPen, Taiwan FactCheck Center, Piyaoba, Radio Free Asia, Piyao.com, Youju, Pengpai, Toutiao] <br>
### For each website, the crawler finds all fact-check articles' urls and save the HTML behind it. 
The HTML will be saved in a folder called `htmls_{site_name}` with a hashed ID as name, and the hash to url mapping is saved in a csv called `lookup_table_{site_name}.csv` <br>
Simply do
```python all_in_one_crawl_new_article.py``` to start crawling. Crawlers are implemented with Selenium whenever the url is not directly visible in the homepage HTML, so expect browsers to pop up when you run this. 
Afterwards, can also do 
```python total_articles.py``` to see some statistics 
