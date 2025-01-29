from .database import connect_to_db, save_to_db, in_db
from dotenv import load_dotenv
import os
from .scraper import fetch_soup, fetch_title, fetch_content, fetch_published_time
from .utils import join_url, reduced_url, url_fragment, is_valid
from .embeddings import model, embedded_vector

class BBCScraper:
    def __init__(self, home_url, db):
        self.db = db
        self.home_url = home_url
        self.links = []
    
    def create_db_entry(self, url):
        soup = fetch_soup(url)
        title = fetch_title(soup)
        published_time = fetch_published_time(soup)
        content = fetch_content(soup)
        if any([x == None for x in [title, published_time, content]]): # Entries are not nullable in our database
            return 
        embedding = embedded_vector(model, content)
        return {'url': url, 'title': title, 'published_time': published_time, 'content': content, 'embedding': embedding}
    
    def get_links(self):
        url = self.home_url
        soup = fetch_soup(url)
        a_tags = soup.find_all('a', {'href':True}) # Get all hyperlinks from a particular page
        for a_tag in a_tags:
            link = join_url(url, a_tag['href'])
            fragment = url_fragment(link)
            if '/articles' in link and fragment == '': # Solely get news articles - no live feeds, podcasts, iplayers etc.
                link = reduced_url(link)
                self.links.append(link)
    
    def save_articles_to_db(self, limit):
        count = 0
        self.get_links()
        links = self.links
        db = self.db
        for link in links:
            entry = self.create_db_entry(link)
            if in_db(db, link) or not is_valid(link) or entry == None:
                continue
            save_to_db(db, entry)
            count += 1
            if count >= limit:
                break
        db.commit() #commit changes to the database
        print(f'{count} articles successfully added to the database')


if __name__ == '__main__':
    load_dotenv()
    db = connect_to_db(os.getenv('DB_HOST'), os.getenv('DB_NAME'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'))
    url = 'https://www.bbc.co.uk/news'
    scraper = BBCScraper(url, db)
    scraper.save_articles_to_db(5)
            





    


