import requests
import urllib
from bs4 import BeautifulSoup
from threading import Thread
import Queue
import multiprocessing
from functools import partial

import consts


class Scraper(Thread):

    def __init__(self, name, queue, search_query):
        Thread.__init__(self)
        self.articles = []
        self.queue = queue
        self.name = name

    def get_articles(self):
        return self.articles

    def run(self):
        while True:
            q = self.queue.get()

articles_queue = Queue.Queue

def scrape_articles(search_query, page_num):
    try:
        url = consts.TECHCRUNCH_URL + str(page_num)
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html)
        soup.prettify()
        articles = soup.find_all('li', {'class': 'river-block'})
        for article in articles:
            article_attrs = article.attrs
            if article.text and search_query.decode("utf-8") in article.text:
                if article_attrs and u'data-permalink' in article_attrs and u'data-sharetitle' in article.attrs:
                    href = article.attrs[u'data-permalink']
                    title = article.attrs[u'data-sharetitle']
                    articles_queue.put((href, title))
    except:
        raise Exception


def scrape(search_query, num_threads=consts.NUM_THREADS):
    func = partial(scrape_articles, search_query)
    pool = multiprocessing.Pool(processes=consts.NUM_THREADS)
    output = pool.map(func, range(consts.NUM_THREADS))
    print output

scrape('is')






