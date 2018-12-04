from bs4 import BeautifulSoup
import requests
import requests_cache
import json
from mongoengine import *
import random


# set up cache
requests_cache.install_cache('state_media_cache')
# set up db
connect('statemediadb')

bias_base_url = 'https://topbottomcenter.com/api/'
rt_base_url = 'https://www.rt.com'
cctv_base_url = 'http://english.cctv.com/'
dw_base_url = 'https://www.dw.com/en/top-stories/s-9097'

class Country(Document):
    name = StringField()

    # def __init__(self, name):
    #     self.name = name
        # dict.__init__(self, name=name)

    def __str__(self):
        return "Country: {}".format(self.name)

class Article(Document):
    title = StringField()
    text = StringField()
    link = StringField()
    bias = FloatField()

    # def __init__(self, title, text, link):
    #     self.title = title
    #     self.text = text
    #     self.link = link
        # dict.__init__(self, title=title, text=text, link=link)
    def __str__(self):
        return "Article: {}\nBias: {}\nText: {}\nLink: {}".format(self.title, self.bias, self.text, self.link)


def get_rt_data():
    response = requests.get(rt_base_url).text
    rt_soup = BeautifulSoup(response, 'html.parser')
    top_articles= rt_soup.find_all('a', attrs={'class', 'main-promobox__link'})
    rt_articles = []
    for article in top_articles:
        if Article.objects(title=article.title) != []:
            title = article.text.strip()
            link = rt_base_url + article.get('href')
            text_request = requests.get(link).text
            text_soup = BeautifulSoup(text_request, 'html.parser')
            r_soup = text_soup.find('div', attrs={'class', 'article__text'}).find_all('p')
            text = ""
            for p in r_soup:
                text += p.text
            article = Article(title, text, link, random.random())
            rt_articles.append(article)
            article.save()
            for article in Article.objects:
                print (article.title)
    # save_to_file('rt_data.json', rt_articles)
    # for article in rt_articles:
    #     print (article)
    return ''
#get_rt_data()

def get_cctv_data():
    response = requests.get(cctv_base_url).text
    cctv_soup = BeautifulSoup(response, 'html.parser')
    main_article = cctv_soup.find('div', attrs={'class', 'text'})
    main_article_link = main_article.find('a').get('href')
    cctv_articles = []
    cctv_articles.append(Article(main_article.text, '', main_article_link, random.random())) #get text
    side_articles = cctv_soup.find_all('div', attrs={'class', 'ind_bd'})[1].find_all('div', attrs={'class', 'box'})
    print(side_articles)
    for article in side_articles:
        title = article.find('a').text
        link = article.find('a').get('href')
        text_request = requests.get(link).text
        text_soup = BeautifulSoup(text_request, 'html.parser')
        cctv_soup = text_soup.find('div', attrs={'class', 'text'}).find_all('p')
        text = ""
        for p in cctv_soup:
            text += p.text
        article = Article(title, text, link, random.random())
        article.save()
        cctv_articles.append(article)
    # for article in cctv_articles:
    #     print(article)
    # save_to_file('cctv_data.json', cctv_articles)
#get_cctv_data()
def get_dw_data():
    response = requests.get(dw_base_url).text
    dw_soup = BeautifulSoup(response, 'html.parser')
    main_article = dw_soup.find('div', attrs={'class', 'imgTeaserXL'})
    main_article_link = dw_base_url + main_article.find('a').get('href')
    main_request = requests.get(main_article_link).text
    main_soup = BeautifulSoup(main_request, 'html.parser').find('div', attrs={'class', 'col3'})
    main_title = main_soup.find('h1').text
    text = ""
    for p in main_soup.find_all('p'):
        text += p.text
    dw_articles = []
    dw_articles.append(Article(main_title, text, main_article_link, random.random())) # get_api_bias_values(main_title, text)))
    side_articles = dw_soup.find_all('div', attrs={'class', 'linkList plain'})
    for article in side_articles:
        title = article.find('a').text
        link = dw_base_url + article.find('a').get('href')
        article_request = requests.get(link).text
        article_soup = BeautifulSoup(article_request, 'html.parser')
        article_title = article_soup.find('h1').text
        for p in article_soup.find_all('p'):
            text += p.text
        article = Article(article_title, text, link, random.random()) #get_api_bias_values(article_title, text))
        article.save()
        dw_articles.append(article)
    for article in dw_articles:
        article.save()
        print(article)
# # get data
# get_rt_data()
# get_cctv_data()
# get_dw_data()

#get bias for new values
# def get_api_bias_values(title, text):
#     response = requests.post(bias_base_url, data={'title': title, 'text': text}, headers={'Accept':'application/json'})
#     print(response)
#     return float(response['political_bias'])

# get bias values for articles that are already in the database
# def update_bias_values():
#     for article in Article.objects:
#         article.bias = get_api_bias_values(article.title, article.text)
#         article.save()
#
# update_bias_values()
for article in Article.objects:
    print (article.bias)

        
