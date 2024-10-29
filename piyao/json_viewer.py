import json
from bs4 import BeautifulSoup, NavigableString, Tag

def clean_text(element):
    """ Recursively extracts text from an HTML element and its children, adding line breaks for block-level elements. """
    text = ''
    if isinstance(element, NavigableString):
        return str(element).strip()
    if isinstance(element, Tag):
        if element.name in ['p', 'div', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']:
            text += '\n'
        for child in element:
            text += clean_text(child)
    return text

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
file_path = '/Users/jimmynian/code/AMICA/crawlers/piyao/all_articles.json'
json_data = read_json_file(file_path)
# json_str = json.dumps(json_data)

# # Decode the Unicode sequences
# decoded_str = json.loads(json_str)

if __name__ == '__main__':
    url = 'https://www.piyao.org.cn/2020-04/20/c_1210578194.htm'
    example_json = [d for d in json_data if d['url'] == url][0]
    
    print("ext1:", example_json['ext1'])
    print("ext2:", example_json['ext2'])
    print("ext3:", example_json['ext3'])
    print("ext4:", example_json['ext4'])
    print("ext5:", example_json['ext5'])
    print("ext6:", example_json['ext6'])
    print("ext7:", example_json['ext7'])
    print("ext8:", example_json['ext8'])
    print("source:", example_json['source'])
    print("sourceDesc:", example_json["sourceDesc"])
    print("type:", example_json['type'])
    print("typeDesc:", example_json["typeDesc"])
    print("city:", example_json['city'])
    print("cityDesc:", example_json["cityDesc"])
    print("publishTime:", example_json['publishTime'])
    print("createDate:", example_json['createDate'])
    print("reprint:", example_json['reprint'])
    print("repeatCount:", example_json['repeatCount'])
    print("tag:", example_json['tag'])

    print("titel:", example_json['title'])
    print("summary:", example_json['summary'])
    soup = BeautifulSoup(example_json['content'], 'html.parser')
    # Extract and clean text from the parsed HTML
    extracted_text = clean_text(soup)
    cleaned_text = '\n'.join(line.strip() for line in extracted_text.splitlines() if line.strip())
    # Print the cleaned text
    print("content:", cleaned_text)
