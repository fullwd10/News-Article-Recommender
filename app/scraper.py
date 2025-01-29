from bs4 import BeautifulSoup
import requests, re

def fetch_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def fetch_title(soup):
    old_title = soup.find('title').text
    title, i = '', 0
    while old_title[i] != '-': # old_title of the form "some title - BBC News"
        title += old_title[i]
        i += 1
    return title


def fetch_published_time(soup):
    try:
        soup.find('time')['datetime'] # Article may not have a published time
    except TypeError:
        return None 
    return soup.find('time')['datetime']

def fetch_content(soup):
    content = ''
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        if paragraph.find('i') != None: # Italic text marks end of article content 
            break
        content += paragraph.text + '\n'

    content = re.sub("\xe2\x80\x93", "-", content) # Replaces unrecoginsed em dashes with hyphens
    return content