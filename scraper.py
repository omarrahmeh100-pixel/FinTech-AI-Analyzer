import requests
from bs4 import BeautifulSoup

from sqlalchemy.orm import Session
from sqlalchemy import select
from models import engine, News

from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

Header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"}


 
def scraping_hackernews(num_pages):
    all_articles = []
    # r now holds all the info inside the link like (pagecode, headers, status code, cookies), r is an object now
    for p in range (1, num_pages+1):
        logging.info(f"Scraping page {p}")
        r = requests.get(f"https://news.ycombinator.com/news?p={p}") # new pagination part in the link is (news?p={p})
        # now we check for errors if it shows 200 then we are fine
        print(r.status_code)
        # r.text stores all the html the server sends, and BeautifulSoup turns the messy string into a structred tree using html parsing technique 
        soup = BeautifulSoup(r.text,"html.parser")
    

        # now headline has all the titlelines inside the webpage we used span tags to cathc them
        headlines = soup.find_all("span", class_= "titleline")
        data_list = []
        for item in headlines:
            title = item.text
            # We need the link again
            link = item.find('a').get('href')
            currentdate = datetime.now().strftime("%Y-%m-%d")
            # We pack it into a dictionary
            article = {   # NEW dictionary every time
                "title": title,
                "link": link,
                "source": "hacker-news",
                "published_date": currentdate 
            }
            data_list.append(article)
        all_articles.extend(data_list)
        
    return all_articles

def scrape_yahoo():
    r = requests.get("https://finance.yahoo.com/topic/stock-market-news/", headers= Header)
    logging.info(f"status code of the request: {r.status_code}")
    soup = BeautifulSoup(r.text, 'html.parser')
    headlines = soup.find_all('div', class_ = 'content yf-e6re4u')
    data_list = []
    for headline in headlines:
        
        currentdate = datetime.now().strftime("%Y-%m-%d")
        link = headline.find('a')
        title = headline.find('h3',class_ = 'clamp yf-e6re4u')
        # 1. SAFETY CHECK 
        # Sometimes find() returns 'None' (e.g., if it's an Ad, not an article).
        # If we try to use .text on None, the script CRASHES.
        # "continue" means: "Ignore this bad item, jump to the top of the loop for the next one.
        
        if not link or not title:
            continue
        title = title.text
        link = link.get('href')
        # 3. DATA CLEANING (The "Repair Shop")
        # Yahoo often gives "Relative Links" (e.g., "/news/story-123").
        # We cannot save that! We need the "Absolute Link" (full website).
        # If it starts with '/', we glue the domain name to the front.
        if link.startswith('/'):
            link = f"https://finance.yahoo.com{link}"

        article_dic = {'title':title,
                       'link':link,
                       'source': "Yahoo Finance",
                       'published_date': currentdate
                       }
        data_list.append(article_dic)
    return data_list



def save_to_db(data):
    added_articles = 0
    skipped_articles = 0
    # 1. THE SESSION
    # The session is a "Staging Area". It is not a connection yet.
    # It waits until we give it a command to talk to the DB.
    session = Session(engine)
    logging.info(f"Saving {len(data)} articles to the Database")

    for article in data:
        # 2. THE CHECK (Immediate Read)
        # We construct a SQL query using the ORM (News.link).
        statement  = select(News).where(News.link == article['link'])
        # 'execute' runs the query immediately because we need the answer now.
        # 'scalar' unboxes the result: It turns [NewsObject] -> NewsObject.
        # If no row is found, it returns None.
        existing_article = session.execute(statement).scalar()
        # 3. THE OBJECT (NewsObject)
        # If found, 'existing_article' is a Python Object representing that database row.
        # We could access 'existing_article.title' here if we wanted!

        if existing_article:
            skipped_articles+=1
            logging.warning(f"Duplicate link skipped: {article['link']}")
            continue
        # 4. THE POPULATION
        # We manually move data from the Raw Dictionary -> Mapped Object.
        
        new_article = News(   # new object every loop like the dic 
            title=article['title'],
            link=article['link'],
            source=article['source'],
            published_date=datetime.strptime(article['published_date'], "%Y-%m-%d") 
            # Note: We convert string date to Python Date object if your model expects DateTime
        )
        # 5. THE STAGING (Delayed Write)
        # .add() does NOT send SQL. It puts the object in the "To-Do" list.
        session.add(new_article)
        added_articles +=1
    # 6. THE TRANSACTION (Atomic Commit)
    
    try:
        # This opens the connection, sends all INSERTs in one batch, and saves.
        session.commit()
        logging.info(f"Saving done. Added articles : {added_articles}. Skipped articles : {skipped_articles}")
    except Exception as e:
        logging.error(f"Error saving batch: {e}")
        # If anything fails (network, constraints), we Undo everything.
        session.rollback()
    finally:
        # We give the connection back to the Engine's pool.
        session.close()



if __name__ == "__main__":
    
    # Makes debugging and testing easier: you can see exactly what you’re about to insert into the database.
    print("--------------------HACKER NEWS--------------------")
    
    scraped_data = scraping_hackernews(2)
    save_to_db(scraped_data)
    print("--------------------Yahoo Finance--------------------")

    yahoo =scrape_yahoo()
    save_to_db(yahoo)
    
    

