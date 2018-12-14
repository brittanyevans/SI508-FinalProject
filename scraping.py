from countries_articles import *
from secrets import db_vals
from bs4 import BeautifulSoup
import requests
import requests_cache
import json
from mongoengine import *
import random
import datetime

# set up cache
requests_cache.install_cache('state_media_cache')
# set up db
connect(db_vals['name'], host=db_vals['host'], port=db_vals['port'], username=db_vals['username'], password=db_vals['password'])

bias_base_url = 'https://topbottomcenter.com/api/'
rt_base_url = 'https://www.rt.com'
cctv_base_url = 'http://english.cctv.com/'
dw_base_url = 'https://www.dw.com/en/top-stories/s-9097'

# when API is back, remove the random number and the use post requests below
def get_api_bias_values(title, text):
    try:
        request_post = requests.post(bias_base_url, data={'title': title, 'text': text}, headers={'Accept':'application/json'})
        response = request_post.json()
        return float(response['political_bias'])
    except:
        return round(random.uniform(-1.0, 1.0),3)

# get bias values for articles that are already in the database
def update_bias_values():
    for article in Article.objects:
        article.bias = get_api_bias_values(article.title, article.text)
        article.save()

# # update the existing country values on articles in the database
def update_country_values():
    for article in Article.objects:
        if 'rt.' in article.link:
            country = Country.objects(name="russia")[0]
            if article not in country.articles:
                country.articles.append(article)
                country.save()
        elif 'english.cctv.' in article.link:
            print('cctv')
            country = Country.objects(name="china")[0]
            if article not in country.articles:
                country.articles.append(article)
                country.save()
        elif 'dw.com/en' in article.link:
            country = Country.objects(name="germany")[0]
            if article not in country.articles:
                country.articles.append(article)
                country.save()

#update_country_values()

def get_rt_data():
    response = requests.get(rt_base_url).text
    rt_soup = BeautifulSoup(response, 'html.parser')
    top_articles= rt_soup.find_all('a', attrs={'class', 'main-promobox__link'})
    rt_articles = []
    for article in top_articles:
        title = article.text.strip()
        db_articles = Article.objects(title=title)
        if len(db_articles) == 0:
            link = rt_base_url + article.get('href')
            text_request = requests.get(link).text
            text_soup = BeautifulSoup(text_request, 'html.parser')
            article_text = text_soup.find('div', attrs={'class', 'article__text'})
            if article_text is not None:
                r_soup = article_text.find_all('p')
                text = ""
                for p in r_soup:
                    text += p.text
                article = Article(title, text, link, get_api_bias_values(title, text))
                rt_articles.append(article)
                article.save()
        else:
            rt_articles.append(db_articles[0])
    if len(Country.objects(name="russia")) == 0:
        country = Country(name="russia",articles=rt_articles)
    else:
        country = Country.objects(name="russia")[0]
        country.articles += rt_articles
        country.articles = list(set(country.articles))
    country.save()
    return rt_articles

def get_cctv_data():
    cctv_articles = []
    response = requests.get(cctv_base_url).text
    cctv_soup = BeautifulSoup(response, 'html.parser')
    main_article = cctv_soup.find('div', attrs={'class', 'text'})
    main_article_title = main_article.text
    db_main_articles = Article.objects(title=main_article_title)
    if (len(db_main_articles) == 0):
        main_article_link = main_article.find('a').get('href')
        text_request = requests.get(main_article_link).text
        text_soup = BeautifulSoup(text_request, 'html.parser')
        p_soup = text_soup.find('div', attrs={'class', 'text'}).find_all('p')
        text = ""
        for p in p_soup:
            text += p.text
        main_article = Article(main_article_title, text, main_article_link, get_api_bias_values(main_article_title, text))
        main_article.save()
    else:
        main_article = db_main_articles[0]
    cctv_articles.append(main_article)

    side_articles = cctv_soup.find_all('div', attrs={'class', 'ind_bd'})[1].find_all('div', attrs={'class', 'box'})
    for article in side_articles:
        title = article.find('a').text
        db_articles = Article.objects(title=title)
        if len(db_articles) == 0:
            link = article.find('a').get('href')
            text_request = requests.get(link).text
            text_soup = BeautifulSoup(text_request, 'html.parser')
            cctv_soup = text_soup.find('div', attrs={'class', 'text'}).find_all('p')
            text = ""
            for p in cctv_soup:
                text += p.text
            article = Article(title, text, link, get_api_bias_values(title, text))
            article.save()
        else:
            article = db_articles[0]
        cctv_articles.append(article)
    if len(Country.objects(name="china")) == 0:
        country = Country(name="china",articles=cctv_articles)
    else:
        country = Country.objects(name="china")[0]
        country.articles += cctv_articles
        country.articles = list(set(country.articles))
    country.save()
    return cctv_articles

def get_dw_data():
    dw_articles = []
    response = requests.get(dw_base_url).text
    dw_soup = BeautifulSoup(response, 'html.parser')
    main_article = dw_soup.find('div', attrs={'class', 'imgTeaserXL'})
    main_article_link = dw_base_url + main_article.find('a').get('href')
    db_articles = Article.objects(link=main_article_link)
    if len(db_articles) == 0:
        main_request = requests.get(main_article_link).text
        main_soup = BeautifulSoup(main_request, 'html.parser').find('div', attrs={'class', 'col3'})
        main_title = main_soup.find('h1').text
        main_text = ""
        for p in main_soup.find_all('p'):
            main_text += p.text
        main_article = Article(main_title, main_text, main_article_link, get_api_bias_values(main_title, main_text))
        main_article.save()
    else:
        main_article = db_articles[0]
    dw_articles.append(main_article)
    side_articles = dw_soup.find_all('div', attrs={'class', 'linkList plain'})
    for article in side_articles:
        title = article.find('a').text
        link = dw_base_url + article.find('a').get('href')
        db_articles = Article.objects(link=link)
        if len(db_articles) == 0:
            article_request = requests.get(link).text
            article_soup = BeautifulSoup(article_request, 'html.parser')
            article_title = article_soup.find('h1').text
            text = ''
            for p in article_soup.find_all('p'):
                text += p.text
            article = Article(article_title, text, link, get_api_bias_values(article_title, text)) #get_api_bias_values(article_title, text))
            article.save()
        else:
            article = db_articles[0]
        dw_articles.append(article)
    if len(Country.objects(name="germany")) == 0:
        country = Country(name="germany",articles=dw_articles)
    else:
        country = Country.objects(name="germany")[0]
        country.articles += dw_articles
        country.articles = list(set(country.articles))
    country.save()
    return dw_articles

# get data
# get_rt_data()
# get_cctv_data()
# get_dw_data()

#pull in json files
# rt_data = open('rt_data.json', 'r')
# data = json.loads(rt_data)
# new_articles = []
# for article in data:
#     if article not in Article.objects:
#         title = article['title']
#         text = article['text']
#         link = article['link']
#         article = Article( title, text, link, get_api_bias_values(title, text), '2018-12-04')
#         article.save()
#     if len(Country.objects(name="russia")) == 0:
#         country = Country(name="russia",articles=new_articles)
#     else:
#         country = Country.objects(name="russia")[0]
#         country.articles += new_articles
#         country.articles = list(set(country.articles))
#     country.save()
# rt_data.close()
