import requests
from bs4 import BeautifulSoup
import re

def BOJCrawl(url):
    try:
        plainCode = requests.get(url,timeout=None)
    except:
        return False
    plainText = plainCode.text
    soup = BeautifulSoup(plainText, 'html.parser')
    titletag = soup.select('head > title')
    title = titletag[0].string
    if title == 'Baekjoon Online Judge':
        return None
    else:
        return title
