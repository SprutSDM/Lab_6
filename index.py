# encoding: utf8
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
from bottle import route, run, template, request, post, get, redirect

import scripts
import classificator

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
def news_list(page=0):
    print(page)
    per = int(request.query.per or PER_PAGE)
    start = max(0, (page - 1) * per)
    news = s.query(News).filter(News.label == None).all()
    if per <= 0 or start >= len(news): # if bad request
        redirect('/news/page1')
        return
    rows = news[start:start+per]
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

@route('/recomendations')
def recomendations():
    fitted_news = s.query(News).filter(News.label != None).all()
    news = s.query(News).filter(News.label == None).all()
    nbc = classificator.NaiveBayesClassifier(0.05)
    X = list()
    y = list()
    for new in fitted_news:
        X.append(scripts.clean(new.title))
        y.append(new.label)
    nbc.fit(X, y)
    predict_news = nbc.predict([scripts.clean(new.title) for new in news])
    sort_news = list()
    for i in range(len(news)):
        if predict_news[i] == 'good':
            mark = 0
        elif predict_news[i] == 'maybe':
            mark = 1
        elif predict_news[i] == 'never':
            mark = 2
        sort_news.append([mark, -news[i].points, -news[i].comments,
                          news[i].author, news[i].title, news[i].url])
    sort_news.sort()
    return template('recomendation_news_template', rows=sort_news)

engine = create_engine("sqlite:///news.db")
Base.metadata.create_all(bind=engine)
session = sessionmaker(bind=engine)
s = session()
print(s.query(News).count())
url = 'https://habrahabr.ru/flows/develop/all/'

run(host='localhost', port=8080)
#get_all_news(s)