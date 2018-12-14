from secrets import plotly_credentials
from mongoengine import *
from scraping import Article, Country
from interface import *
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import datetime

plotly.tools.set_credentials_file(username=plotly_credentials['username'], api_key=plotly_credentials['api_key'])

date_values = []
bias_values = []
marker_values = []

def plot():
    N = len(bias_values)
    bias = bias_values
    date = date_values
    text = marker_values

    # Create a trace
    trace = go.Scatter(
        x = bias,
        y = date,
        mode = 'markers',
        text = text
    )

    data = [trace]
    py.plot(data, filename='basic-line')
# plot article from all countries for the day
def plot_day_all():
    for country in Country.objects:
        for article in country.articles:
            if article.date.strftime('%Y-%m-%d') == datetime.datetime.today().strftime('%Y-%m-%d'):
                    bias_values.append(article.bias)
                    date_values.append(article.date.strftime('%Y-%m-%d'))
                    marker_values.append(country.name.capitalize() + ': "' + article.title + '"')
    plot()
    bias_values.clear()
    date_values.clear()
    marker_values.clear()

#plot all articles from all countries
def plot_all():
    for country in Country.objects:
        for article in country.articles:
            bias_values.append(article.bias)
            date_values.append(article.date.strftime('%Y-%m-%d'))
            marker_values.append(country.name.capitalize() + ': "' + article.title + '"')
    plot()
    bias_values.clear()
    date_values.clear()
    marker_values.clear()

# plot articles from one country for the day
def plot_country_all(country_name):
    country = Country.objects(name=country_name)[0]
    for article in country.articles:
        if type(article) == type(Article()):
            bias_values.append(article.bias)
            date_values.append(article.date.strftime('%Y-%m-%d'))
            marker_values.append(country_name.capitalize() + ': "' + article.title + '"')
    plot()
    bias_values.clear()
    date_values.clear()
    marker_values.clear()

# plot articles for one country for one day
def plot_country_day(country_name):
    country = Country.objects(name=country_name)[0]
    for article in country.articles:
        if article.date.strftime('%Y-%m-%d') == datetime.datetime.today().strftime('%Y-%m-%d'):
            bias_values.append(article.bias)
            date_values.append(article.date.strftime('%Y-%m-%d'))
            marker_values.append(country_name.capitalize() + ': "' + article.title + '"')
    plot()
    bias_values.clear()
    date_values.clear()
    marker_values.clear()
