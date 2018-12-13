import unittest
import requests_mock
from unittest.mock import MagicMock
from scraping import *
from my_plotly import *
from mongoengine import *
from mongoengine.context_managers import switch_db

# import mongomock
#
# class test_database_mongoengine(unittest.TestCase):
#     connect('mongoenginetest', host='mongomock://localhost')
#     conn = get_connection()

def get_html_text(filename):
    f = open(filename)
    html = f.read()
    f.close()
    return html


class test_rt_article_scraping(unittest.TestCase):
    def test_returns_correct_number_of_articles_in_list(self):
        articles = get_rt_data()
        self.assertTrue(len(articles) == 3)
        self.assertEqual(type(articles), type([]))

    def test_save_article_to_database(self):
        articles = get_rt_data()
        for article in articles:
            self.assertTrue(len(Article.objects(title=article.title)) != 0)

    @requests_mock.Mocker()
    def test_saved_articles_do_not_make_requests(self, m):
        home_page = get_html_text('mock_html/rt/home.html')
        m.get('https://www.rt.com/', text=home_page)

        article_1 = get_html_text('mock_html/rt/article-1.html')
        m.get('https://www.rt.com/article-1', text=article_1)

        article_2 = get_html_text('mock_html/rt/article-2.html')
        m.get('https://www.rt.com/article-2', text=article_2)

        article_3 = get_html_text('mock_html/rt/article-3.html')
        m.get('https://www.rt.com/article-3', text=article_3)

        Article.drop_collection()
        get_rt_data() # makes one request for the home page, one request for each of the three articles
        get_rt_data() # makes one request for the home page, no requests for each of the three articles
        self.assertEqual(m.call_count, 5)

class test_cctv_article_scraping(unittest.TestCase):
    def test_returns_correct_number_of_articles_in_list(self):
        articles = get_cctv_data()
        self.assertTrue(len(articles) == 2)
        self.assertEqual(type(articles), type([]))

    def test_save_article_to_database(self):
        articles = get_cctv_data()
        for article in articles:
            self.assertTrue(len(Article.objects(title=article.title)) != 0)

    @requests_mock.Mocker()
    def test_saved_articles_do_not_make_requests(self, m):
        home_page_c = get_html_text('mock_html/cctv/home.html')
        m.get('http://english.cctv.com/', text=home_page_c)

        article_1_c = get_html_text('mock_html/cctv/main-article.html')
        m.get('http://english.cctv.com/main-article.html', text=article_1_c)

        article_2_c = get_html_text('mock_html/cctv/side-article.html')
        m.get('http://english.cctv.com/side-article.html', text=article_2_c)

        Article.drop_collection()
        get_cctv_data() # makes one request for the home page, one request for each of the two articles
        get_cctv_data() # makes one request for the home page, no requests for each of the two articles
        self.assertEqual(m.call_count, 4)

class test_dw_article_scraping(unittest.TestCase):
    def test_returns_correct_number_of_articles_in_list(self):
        articles = get_dw_data()
        self.assertTrue(len(articles) == 2)
        self.assertEqual(type(articles), type([]))

    def test_save_article_to_database(self):
        articles = get_dw_data()
        for article in articles:
            self.assertTrue(len(Article.objects(title=article.title)) != 0)

    @requests_mock.Mocker()
    def test_saved_articles_do_not_make_requests(self, m):
        home_page_d = get_html_text('mock_html/dw/home.html')
        m.get('https://www.dw.com/en/top-stories/s-9097', text=home_page_d)

        article_1_d = get_html_text('mock_html/dw/main-article.html')
        m.get('https://www.dw.com/en/top-stories/s-9097/main-article', text=article_1_d)

        article_2_d = get_html_text('mock_html/dw/side-article.html')
        m.get('https://www.dw.com/en/top-stories/s-9097/side-article', text=article_2_d)

        Article.drop_collection()
        get_dw_data() # makes one request for the home page, one request for each of the two articles
        get_dw_data() # makes one request for the home page, no requests for each of the two articles
        self.assertEqual(m.call_count, 4)

class test_get_bias_values(unittest.TestCase):
    def test_api_call(self):
        # I can't test API values for requests that I can't make.
        self.assertEqual(type(get_api_bias_values('title', 'text')),type(3.0))

class test_article_class(unittest.TestCase):
    def test_article_str_func(self):
        test_article = Article('Title', 'Text', 'Link', 3.0)
        self.assertEqual(str(test_article), "Article: Title\nBias: 3.0\nText: Text\nLink: Link")

class test_country_class(unittest.TestCase):
    def test_str_func(self):
        test_country = Country('Namibia', [])
        self.assertEqual(type(str(test_country)), type('Country: Namibia'))

class test_plotly_mapping(unittest.TestCase):
    ### I can't test that the plots are created correctly, but I can test that the functions don't produce errors.
    def test_plot_for_country_in_day(self):
        Country.drop_collection()
        Article.drop_collection()
        [article_1, article_2, article_3] = [Article("title1", "text1", "link1"), Article("title2", "text2", "link2"), Article("title3", "text3", "link3")]
        article_1.bias = 1.5
        article_1.date = datetime.datetime.today()
        article_1.save()
        article_2.bias = 2.5
        article_2.date = datetime.datetime(2018, 12, 27)
        article_2.save()
        Country('namibia', [article_1, article_2]).save()
        article_3.bias = 2.7
        article_3.date = datetime.datetime(2018, 11, 6)
        article_3.save()
        Country('canada', [article_3]).save()
        plot_country_day('namibia')
        scatter = plotly.graph_objs.Scatter(x = [1.5], y = [datetime.datetime.today().strftime('%Y-%m-%d')], mode = 'markers')
        plotly.plotly.plot.assert_called_with([scatter], filename='basic-line')

    def test_plot_for_country_all(self):
        Country.drop_collection()
        Article.drop_collection()
        [article_1, article_2, article_3] = [Article("title1", "text1", "link1"), Article("title2", "text2", "link2"), Article("title3", "text3", "link3")]
        article_1.bias = 1.5
        article_1.date = datetime.datetime(2018, 9, 10)
        article_1.save()
        article_2.bias = 2.5
        article_2.date = datetime.datetime(2018, 12, 27)
        article_2.save()
        Country('namibia', [article_1, article_2]).save()
        article_3.bias = 2.7
        article_3.date = datetime.datetime(2018, 11, 6)
        article_3.save()
        Country('canada', [article_3]).save()
        plot_country_all('namibia')
        scatter = plotly.graph_objs.Scatter(x = [1.5, 2.5], y = ['2018-09-10', '2018-12-27'], mode = 'markers')
        plotly.plotly.plot.assert_called_with([scatter], filename='basic-line')

    def test_plot_for_day(self):
        Country.drop_collection()
        Article.drop_collection()
        [article_1, article_2, article_3] = [Article("title1", "text1", "link1"), Article("title2", "text2", "link2"), Article("title3", "text3", "link3")]
        article_1.bias = 1.5
        article_1.date = datetime.datetime.today()
        article_1.save()
        article_2.bias = 2.5
        article_2.date = datetime.datetime(2018, 12, 27)
        article_2.save()
        Country('namibia', [article_1, article_2]).save()
        article_3.bias = 2.7
        article_3.date = datetime.datetime.today()
        article_3.save()
        Country('canada', [article_3]).save()
        plot_day_all()
        scatter = plotly.graph_objs.Scatter(x = [1.5, 2.7], y = [datetime.datetime.today().strftime('%Y-%m-%d'),datetime.datetime.today().strftime('%Y-%m-%d')], mode = 'markers')
        plotly.plotly.plot.assert_called_with([scatter], filename='basic-line')

    def test_plot_all(self):
        Country.drop_collection()
        Article.drop_collection()
        [article_1, article_2, article_3] = [Article("title1", "text1", "link1"), Article("title2", "text2", "link2"), Article("title3", "text3", "link3")]
        article_1.bias = 1.5
        article_1.date = datetime.datetime.today()
        article_1.save()
        article_2.bias = 2.5
        article_2.date = datetime.datetime(2018, 12, 27)
        article_2.save()
        Country('namibia', [article_1, article_2]).save()
        article_3.bias = 2.7
        article_3.date = datetime.datetime.today()
        article_3.save()
        Country('canada', [article_3]).save()
        plot_all()
        scatter = plotly.graph_objs.Scatter(x = [1.5, 2.5, 2.7], y = [datetime.datetime.today().strftime('%Y-%m-%d'), "2018-12-27", datetime.datetime.today().strftime('%Y-%m-%d')], mode = 'markers')
        plotly.plotly.plot.assert_called_with([scatter], filename='basic-line')

def setUpModule():
    home_page = get_html_text('mock_html/rt/home.html')
    mock_request.get('https://www.rt.com/', text=home_page)

    article_1 = get_html_text('mock_html/rt/article-1.html')
    mock_request.get('https://www.rt.com/article-1', text=article_1)

    article_2 = get_html_text('mock_html/rt/article-2.html')
    mock_request.get('https://www.rt.com/article-2', text=article_2)

    article_3 = get_html_text('mock_html/rt/article-3.html')
    mock_request.get('https://www.rt.com/article-3', text=article_3)

    home_page_c = get_html_text('mock_html/cctv/home.html')
    mock_request.get('http://english.cctv.com/', text=home_page_c)

    article_1_c = get_html_text('mock_html/cctv/main-article.html')
    mock_request.get('http://english.cctv.com/main-article.html', text=article_1_c)

    article_2_c = get_html_text('mock_html/cctv/side-article.html')
    mock_request.get('http://english.cctv.com/side-article.html', text=article_2_c)

    home_page_d = get_html_text('mock_html/dw/home.html')
    mock_request.get('https://www.dw.com/en/top-stories/s-9097', text=home_page_d)

    article_1_d = get_html_text('mock_html/dw/main-article.html')
    mock_request.get('https://www.dw.com/en/top-stories/s-9097/main-article', text=article_1_d)

    article_2_d = get_html_text('mock_html/dw/side-article.html')
    mock_request.get('https://www.dw.com/en/top-stories/s-9097/side-article', text=article_2_d)

    plotly.plotly.plot = MagicMock(return_value=None)

def tearDownModule():
    Country.drop_collection()
    Article.drop_collection()

if __name__ == '__main__':
    connect('test-db', alias='test')
    with requests_mock.Mocker() as mock_request:
        with switch_db(Article, 'test') as Article:
            with switch_db(Country, 'test') as Country:
                unittest.main()
