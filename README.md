## News-Article-Recommender

### Project Outline
In this personal project I develop a algorithm using **Python** and **PostgreSQL** which forms the basis of a BBC News article recommendation system. The purpose of this project has been to act as an introduction to **web scraping** and to applied **natural language processing** (NLP).

#### Web Scraping
As mentioned, the website I have chosen to scrape is the [BBC News homepage](https://www.bbc.co.uk/news), of which I have used the elegant python library **Beautiful Soup** to do so. The processes involve scraping all the articles links from the home page and then processing the corresponding articles, of which content such as fecthing the title and body of articles can be found in the `scraper.py` file.

Please note, however, that the functions related scraping the website, as found in the scraper.py file, as specific to how the BBC page is written in HTML and is not necessary generalisable to other news websites.

#### Database
For the database I have used **PostgreSQL 17** and the python database adapter **psycopg2**. In the database is where the information of all the scraped articles is stored, namely the url, title, published date, content and the corresponding vector embedding. The associated functions can be found in the `database.py` file. 

#### Vector Embeddings 
In order to store the embeddings on the database, I installed the Postgres vector extension **pgvector** which one can also install via GitHub [here](https://github.com/pgvector). This extension allows us to efficiently perform vector operations on our text embeddings, most notably it enables us to calculate the **cosine distance** between two vectors and thus determine which articles are the most 'similiar' to a given one.

As for actually calculating the vector embedding corresponding to a news article, I have used Jina AI's `jina-embeddings-v2-base-en` model, which can be found [here](https://huggingface.co/jinaai/jina-embeddings-v2-base-en). It has been purposely chosen as it's free to use and supports desriable input sequences of length 8k+. Moreover, the model is extremely simple to use; the associated function found in `embeddings.py` comprises a couple lines with the input the particular model being used and the string of text, and the output being a 768 dimensional vector. 

---
### Setup 
Install the packages needed for this project in a virutal environment via the `requirements.txt` file with the following command: 

```bash
 pip install -r requirements.txt
```

Moreover, the instructions for installing the pgvector extension on a Mac/Linux as found on [GitHub](https://github.com/pgvector) are as follows:
```bash
cd /tmp
git clone --branch v0.8.0 https://github.com/pgvector/pgvector.git
cd pgvector
make
make install # may need sudo
```
---
### Final Notes 

This has been a very enjoyable project, giving me a real insight into the power and flexibility of webscraping to extract useful data from a variety of different sources. Moreover, it has enabled me to actually apply my theoretical knowledge of machine learning and of nlp in particular. I hope in the future to expand on this project, developing a news feed from a range of different news sources for a particular user, which learns from their inputs and recommends articles based on this information. 


