import requests
from bs4 import BeautifulSoup
import re


def DateCrawl(url):
    plainCode = requests.get(url)
    plainText = plainCode.text
    soup = BeautifulSoup(plainText, 'html.parser')
    div = soup.select('div#evt-wrp-2 > div.evt-wrp')[0]
    t = div.select('div.evt-time')[0].text
    parse = re.match('(\d+:\d+.)(...)...',t)
    if parse:
        t = parse.group(2) + ' ' +parse.group(1)
    d = div.select('div.evt-date')[0].text
    return d+t
    
def CFCrawl():
    url = 'http://codeforces.com/contests'
    plainCode = requests.get(url)
    plainText = plainCode.text
    soup = BeautifulSoup(plainText, 'html.parser')
    table = soup.select('div.contestList > div.datatable > div > table')
    trs = table[0].find_all('tr', recursive = False)
    contestList = []
    for i in range(1, min(len(trs),3)):
        tr = trs[i]
        tds = tr.find_all('td', recursive = False)
        roundname = tds[0].string.strip('\r\n ')
        link = tds[2].a.get('href')
        date = DateCrawl(link)
        
        length = tds[3].string.strip('\r\n ')
        remain = tds[4].text.strip('\r\n ')
        contestList.append((roundname, date, length, remain))
    return contestList


