import requests
from bs4 import BeautifulSoup
from time import sleep
import re

def MakeNameDic(List):
    dic = {}
    for i in range(1,len(List)):
        name = List[i][0]
        parse = re.match(r'(\S+)(\s*\S*)\s+([A-Z]{3})\s*(\S*)$',name)
        if parse:
            ctry = parse.group(1)+parse.group(2)
            simbol = parse.group(3)
            dic[ctry]=simbol
            dic[simbol]=simbol
    return dic

def MakeExDic(List):
    dic = {}
    for i in range(1,len(List)):
        name = List[i][0]
        parse = re.match(r'(\S+)(\s*\S*)\s+([A-Z]{3})\s*(\S*)$',name)
        if parse:
            ctry = parse.group(1)+parse.group(2)
            simbol = parse.group(3)
            isHundred = not parse.group(4)==''
            dic[simbol]=(float(List[i][1].replace(',','')),isHundred)
    return dic

def ExchangeCrawl():
    List = []
    try:
        sourceHtml = requests.get("http://info.finance.naver.com/marketindex/?tabSel=exchange#tab_section",timeout=5)
    except:
        return False
    sourceText = sourceHtml.text
    soup = BeautifulSoup(sourceText, 'html.parser')
    info = soup.select('div.exchange_info')[0].text.strip('\n ').replace('\n','/')
    List.append(('info',info))
    try:
        sourceHtml = requests.get("http://info.finance.naver.com/marketindex/exchangeList.nhn",timeout=5)
    except:
        return False
    sourceText = sourceHtml.text
    soup = BeautifulSoup(sourceText, 'html.parser')
    table = soup.select('tbody')
    trs = table[0].find_all('tr',recursive = False)
    
    for tr in trs:
        tds = tr.find_all('td',recursive = False)
        con = []
        for i in range(2):
            td = tds[i]
            con.append(td.text.strip('\n\r\t'))
        name = con[0]
        
        parse = re.match(r'(\S+)(\s*\S*)\s+([A-Z]{3})\s*(\S*)$',name)
        if parse:
            ctry = parse.group(1)+parse.group(2)
            simbol = parse.group(3)
            isHundred = not parse.group(4)==''
            List.append((name,con[1],isHundred))
    List.append(('한국 KRW','1.00',False))
    return List

def WriteTable(List):
    strlist=[]
    for x in List:
        strlist.append('|'.join(x))
    string = '\n'.join(strlist)
    f=open("exchange_table.txt",mode = 'w',encoding = 'utf8')
    f.write(string)
    f.close()



while True:
    List = ExchangeCrawl()
    if List:
        break
