# encoding: utf8
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
from bottle import route, run, template, request, post, get, redirect

import scripts

#CONSTANTS
PER_PAGE = 10


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


@route('/')
@route('/news')
@route('/news/')
@route('/news/page<page:int>')
def news_list(page = 0):
    print(page)
    per = int(request.query.per or PER_PAGE)
    start = max(0, (page - 1) * per)
    if per <= 0 or start >= s.query(News).count(): # if bad request
        redirect('/news/page1')
        return
    rows = s.query(News).filter(News.label == None).all()[start:start+per]
    return template('news_template', rows=rows)

@route('/update_news')
def update_news():
    scripts.update_news()
    redirect('/news')

@route('/add_label/')
def add_label():
    label = request.query.label
    ID = request.query.id
    print(label, ID)
    s.query(News).get(ID).label = label
    s.commit()
    redirect('/news')


engine = create_engine("sqlite:///news.db")
Base.metadata.create_all(bind=engine)
session = sessionmaker(bind=engine)
s = session()
print(s.query(News).count())
url = 'https://habrahabr.ru/flows/develop/all/'

run(host='localhost', port=8080)
#get_all_news(s)