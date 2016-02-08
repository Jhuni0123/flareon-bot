import requests
from bs4 import BeautifulSoup
import re


def DateCrawl(url):
    try:
        plainCode = requests.get(url,timeout=5)
    except:
        return False
    plainText = plainCode.text
    soup = BeautifulSoup(plainText, 'html.parser')
    div = soup.select('div#evt-wrp-2 > div.evt-wrp')[0]
    t = div.select('div.evt-time')[0].contents[0]
    apm = div.select('span.evt-apm')[0].contents[0].strip('\xa0\r\n ')
    d = div.select('div.evt-date')[0].contents[0].strip('\xa0')
    return d+' '+apm+' '+t
    
def CFCrawl():
    url = 'http://codeforces.com/contests'
    try:
        plainCode = requests.get(url,timeout=5)
    except:
        return False
    plainText = plainCode.text
    soup = BeautifulSoup(plainText, 'html.parser')
    table = soup.select('div.contestList > div.datatable > div > table')
    trs = table[0].find_all('tr', recursive = False)
    contestList = []
    for i in range(1, min(len(trs),3)):
        tr = trs[i]
        tds = tr.find_all('td', recursive = False)
        roundname = tds[0].contents[0].strip('\r\n ')
        link = tds[2].a.get('href')
        date = DateCrawl(link)
        if date == False:
            return False
        length = tds[3].contents[0].strip('\r\n ')
        remain = tds[4].text.strip('\r\n ').replace('\n',' ')
        contestList.append((roundname, date, length, remain))
    return contestList

#CFCrawl()
