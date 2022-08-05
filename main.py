#! python3
import logging
import re
from logging import basicConfig, info, error, warning, debug

import requests
from bs4 import BeautifulSoup

basicConfig(format='%(levelname)s %(asctime)s: %(message)s ', datefmt='%d/%m/%Y %I:%M:%S', encoding="utf-8",
            level=logging.DEBUG)

site_url = "http://www.jumia.com.tn"


def connect(url):
    info(f"Connecting to {url} ...")
    try:
        h = requests.get(url)
        b = BeautifulSoup(h.text, "html.parser")
        info("Connected")
        return h, b
    except Exception as e:
        error("Connection failed")
        error(str(e))
        return


def search_product():
    nb = 0
    search = input("search : >>> ")
    if search:
        url = site_url + "/catalog/?q=" + "+".join(search.split())
        info(f"search terms: {'+'.join(search.split())}")
        links = get_links(url)
        for link in links:
            _, b = connect(link)
            articles = b.find_all("article")
            if articles:
                for article in articles:
                    try:
                        name = article.find('h3', {'class': 'name'}).text
                        price = article.find('div', {'class': 'prc'}).text
                        old = article.find('div', {'class': 'old'})
                        discount = article.find('div', {'class': 'bdg _dsct _sm'})
                        href = article.find('a', {'class':'core'})
                        print('article \t: ', name)
                        print('price \t\t: ', price)
                        if old:
                            print('old price\t: ', old.text)
                            print('discount \t: ', discount.text)
                        if href:
                            print('href \t\t: ', site_url+href['href'])
                        print('-' * 50)
                        nb += 1
                    except Exception as e:
                        warning(str(e))
                        continue
        print(f'found {nb} articles')
    else:
        input("no search terms were provided")
        exit()


def get_links(url):
    links = []
    if url:
        _, b = connect(url)
        try:
            last_page = b.find("a", {"aria-label": "Dernière page"})["href"]
        except Exception as e:
            warning(str(e))
            last_page = None
        if last_page:
            reg = re.compile(r"page=(\d+)#")
            last_page_number = int(reg.search(last_page).group(1))
            for i in range(1, last_page_number + 1):
                link = url + f"&page={i}#catalog-listing"
                debug(f"created link {link}")
                links.append(link)
            return links
        else:
            link = url + "&page=1#catalog-listing"
            debug(f"created link {link}")
            links.append(link)
            return links


if __name__ == "__main__":
    search_product()
