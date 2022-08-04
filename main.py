#! python3
from logging import basicConfig, info, error, INFO

import requests
from bs4 import BeautifulSoup

basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S', encoding="utf-8",
            level=INFO)

site_url = "http://www.jumia.com.tn/"
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
    search = input("search : >>> ")
    if search:
        url = site_url + "+".join(search.split())
        info(f"search terms: {'+'.join(search.split())}")
        connect(url)
    else:
        input("no search terms were provided")
        exit()



if __name__ == "__main__":
    search_product()
