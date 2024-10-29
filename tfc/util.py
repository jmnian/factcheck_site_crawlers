import os
import hashlib
import csv
from datetime import datetime

def save_all_htmls(SAVE_DIR, METADATA_FILE, html_tuples):
    # SAVE_DIR: Directory to save HTML files
    # METADATA_FILE: Metadata file to store additional information
    # html_tuples: a list of ("https://www.example.com", "<html>...</html>")

    # Ensure the directories exist
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    # Initialize or open the metadata file for writing
    with open(METADATA_FILE, 'a', newline='') as csvfile:
        fieldnames = ['unique_id', 'url', 'crawl_date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Function to save HTML
        def save_html(url, html_content):
            # Create a unique identifier using MD5 hash of the URL
            unique_id = hashlib.md5(url.encode()).hexdigest()

            # Save the HTML content to a file
            with open(os.path.join(SAVE_DIR, f"{unique_id}.html"), "w", encoding="utf-8") as file:
                file.write(html_content)

            # Time now
            current_datetime = datetime.now()
            datetime_str = current_datetime.strftime('%Y_%m_%d_%H:%M:%S')

            # Write metadata information
            writer.writerow({'unique_id': unique_id, 'url': url, 'crawl_date': datetime_str})

        for url, html in html_tuples:
            url_sample = "https://www.example.com"
            html_content_sample = "<html>...</html>"  # This would be fetched from your crawler
            save_html(url, html)


def add(x):
    print(x+x)

if __name__ == '__main__':
    htmls = [("https://www.example.com", "<html>...</html>")]
    save_all_htmls("directory", "metadata_file", htmls)
