# encoding: utf8
from bottle import route, run, template, request, post, get, redirect
from bs4 import BeautifulSoup
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymorphy2
import requests
import string


URL = 'https://habrahabr.ru/flows/develop/all/'
morph = pymorphy2.MorphAnalyzer()
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

def get_news(page):
    news = page.body.find_all('article')
    data = []
    for new in news:
        d = dict()
        title = new.h2.a.text
        author = new.header.a.find_all('span')[-1].text
        url = new.h2.a.get('href')
        comments = new.footer.ul.find_all('li')[-1].a.find_all('span')[1].text
        points = new.footer.ul.find_all('li')[0].div.find_all('span')[1].text
        d['author'] = author
        d['title'] = title
        d['url'] = url
        if comments == 'Комментировать':
            comments = 0
        d['comments'] = int(comments)
        if points != '0':
            points = points[1:]
        d['points'] = int(points)
        data.append(d)
    return data

def get_all_news():
    engine = create_engine("sqlite:///news.db")
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)
    s = session()    

    i = 0
    while i != 100:
        print(URL + 'page' + str(i + 1) + '/')
        r = requests.get(URL + 'page' + str(i + 1) + '/')
        page = BeautifulSoup(r.text, 'html.parser')
        news = get_news(page)
        for elem in news:
            new = News(**elem)
            s.add(new)
        i += 1
    s.commit()

def update_news():
    engine = create_engine("sqlite:///news.db")
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)
    s = session()

    i = 0
    run = True
    while i != 100 and run:
        print(URL + 'page' + str(i + 1) + '/')
        r = requests.get(URL + 'page' + str(i + 1) + '/')
        page = BeautifulSoup(r.text, 'html.parser')
        news = get_news(page)
        for elem in news:
            if len(s.query(News).filter(News.url.contains(elem['url'])).all()) == 1:
                run = False
                break
            new = News(**elem)
            s.add(new)
        i += 1
    s.commit()


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator).lower()

def morph_analyzer(s):
    return [morph.parse(word)[0].normal_form for word in s.split()]