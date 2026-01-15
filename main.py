from fastapi import FastAPI
from sqlalchemy.orm import Session
from models import engine,News
from sqlalchemy import select

app = FastAPI(
    title= "TradeSentinel API",
    version= "0.1.0",
    description="A Market Intelligence API that serves financial news."

)

@app.get('/')
def read_root():
    return {"status": "online", "message": "TradeSentinel is watching."}

@app.get('/health')
def health_check():
    return  {"status" : "Okay"}

@app.get('/news')
def get_news(limit : int = 20, offset : int = 0):
    with Session(engine) as session:
        statement = select(News).limit(limit).offset(offset)
        result = session.execute(statement).scalars().all()
    return result 
