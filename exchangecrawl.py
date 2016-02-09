import requests
from bs4 import BeautifulSoup
from time import sleep
def ExchangeCrawl():
    try: 
        sourceHtml = requests.get("http://info.finance.naver.com/marketindex/exchangeList.nhn",timeout=5)
    except:
        return False
    sourceText = sourceHtml.text
    soup = BeautifulSoup(sourceText, 'html.parser')
    table = soup.select('tbody')
    trs = table[0].find_all('tr',recursive = False)
    List=[]
    for tr in trs:
        tds = tr.find_all('td',recursive = False)
        con = []
        for i in range(8):
            td = tds[i]
            con.append(td.text.strip('\n\r\t'))
        List.append(tuple(con))
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
    ExchangeCrawl()
    sleep(60*60)
