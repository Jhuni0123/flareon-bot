import requests
from bs4 import BeautifulSoup
import re

def BOJCrawl(url):
    plainCode = requests.get(url,timeout=10)
    plainText = plainCode.text
    soup = BeautifulSoup(plainText, 'html.parser')
    titletag = soup.select('head > title')
    title = titletag[0].string
    if title == 'Baekjoon Online Judge':
        return False
    else:
        return title
