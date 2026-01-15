from sqlalchemy import Integer, String, DateTime, Column, create_engine
from sqlalchemy.orm import declarative_base
from config import url
import logging
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

engine = create_engine(url)

Base = declarative_base()

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key= True) # Integer + PK means autoincrement 
    title = Column(String)
    link = Column(String, unique= True)
    source = Column(String)
    published_date = Column(DateTime)


if __name__ == "__main__":
    # safe to run multi times because sqlalchemy has if not exist under the hood 
    Base.metadata.create_all(engine)
    logging.info("Table Created Successfully")
    