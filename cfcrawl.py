import requests, json
from bs4 import BeautifulSoup
import re, time


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

def CFAPI():
    wdays = ['월','화','수','목','금','토','일']
    try:
        #stime = time.time()
        plainCode = requests.get('http://codeforces.com/api/contest.list',timeout = 5)
        #etime = time.time()
        #print(etime-stime)
        now = round(time.time())
    except:
        return False
    plainText = plainCode.text
    Dic = json.loads(plainText)
    if Dic['status']=='OK':
        List = Dic['result']
    else:
        return False
    conList = []
    for cont in List:
        if cont['phase'] == 'FINISHED':
            break
        name = cont['name']
        phase = cont['phase']
        durationsec = round(cont['durationSeconds'])
        duration = '%02d:%02d' % (durationsec//60//60%24, durationsec//60%60)
        startTimesec = cont['startTimeSeconds']
        startDate = time.strftime("%Y년 %m월 %d일",time.localtime(startTimesec))
        startTime = time.strftime("%H:%M",time.localtime(startTimesec))
        wday = wdays[time.localtime(startTimesec).tm_wday] + '요일'
        start = '%s %s %s' % (startDate, wday, startTime)  
        relsec = round(cont['relativeTimeSeconds'])
        if relsec>0:
            remainsec = durationsec - relsec
        else:
            remainsec = -relsec
        remain = '%02d:%02d:%02d' % (remainsec//60//60%24, remainsec//60%60, remainsec%60)
        if remainsec//60//60//24 > 0:
            remain = '%dday%s ' % (remainsec/60/60/24, '' if remainsec//60//60//24 == 1 else 's') + remain
        conList = [(name,start,duration,phase,remain)] + conList[:]
    return conList


CFAPI()
