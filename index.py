# encoding: utf8
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
from bottle import route, run, template, request, post, get, redirect

Base = declarative_base()

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key = True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)

@route('/news')
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)

@route('/add_label/')
def add_label():
    label = request.query.label
    ID = request.query.id
    print(label, ID)
    redirect('/news')

engine = create_engine("sqlite:///news.db")
Base.metadata.create_all(bind=engine)
session = sessionmaker(bind=engine)
s = session()
url = 'https://habrahabr.ru/flows/develop/all/'

run(host='localhost', port=8080)
#get_all_news(s)