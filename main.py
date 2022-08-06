#! python3
import logging
import os
import re
import shelve
import sys
from logging import basicConfig, info, error, warning, debug

import requests
from bs4 import BeautifulSoup

basicConfig(format='%(levelname)s %(asctime)s: %(message)s ', datefmt='%d/%m/%Y %I:%M:%S', encoding="utf-8",
            level=logging.WARN)
logging.disable(logging.WARN)

site_url = "http://www.jumia.com.tn"


def clear():
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')


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


def search_product(s):
    clear()
    results = []
    nb = 0
    if s:
        url = site_url + "/catalog/?q=" + "+".join(s.split())
        info(f"search terms: {'+'.join(s.split())}")
        links = get_links(url)
        for link in links:
            _, b = connect(link)
            articles = b.find_all("article")
            if articles:
                for article in articles:
                    res = []
                    try:
                        name = article.find('h3', {'class': 'name'}).text
                        if name:
                            res.append(name)
                            print('article \t: ', name)
                        price = article.find('div', {'class': 'prc'}).text
                        if price:
                            res.append(price)
                            print('price \t\t: ', price)
                        old = article.find('div', {'class': 'old'})
                        if old:
                            print('old price\t: ', old.text)
                            res.append(old.text)
                        discount = article.find('div', {'class': 'bdg _dsct _sm'})
                        if discount:
                            print('discount \t: ', discount.text)
                            res.append(discount.text)
                        href = article.find('a', {'class': 'core'})
                        if href:
                            print('href \t\t: ', site_url + href['href'])
                            res.append(site_url + href['href'])
                        if name:
                            print('-' * 50)
                            nb += 1
                            results.append(res)
                    except Exception as e:
                        warning(str(e))
                        continue
        print(f'found {nb} articles')
        return results
    else:
        input("no search terms were provided")
        exit()
        return None


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
    search = input("search : >>> ")
    products = search_product(search)
    result_file = shelve.open('results')
    # print(list(result_file.keys()))
    result_file[search] = products
    result_file.close()
