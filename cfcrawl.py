import requests, json
from bs4 import BeautifulSoup
import re, time


def CFContestList():
    wdays = ['월','화','수','목','금','토','일']
    try:
        plainCode = requests.get('http://codeforces.com/api/contest.list',timeout = 5)
        now = round(time.time())
        Dic = json.loads(plainCode.text)

    except:
        return False
    if Dic.get('status')=='OK':
        List = Dic.get('result')
    else:
        return False
    conList = []
    for cont in List:
        if cont['phase'] != 'FINISHED':
            name = cont.get('name')
            phase = cont.get('phase')
            durationsec = round(cont.get('durationSeconds'))
            duration = '%02d:%02d' % (durationsec//60//60%24, durationsec//60%60)
            startTimesec = cont.get('startTimeSeconds')
            if startTimesec:
                startDate = time.strftime("%Y년 %m월 %d일",time.localtime(startTimesec))
                startTime = time.strftime("%H:%M",time.localtime(startTimesec))
                wday = wdays[time.localtime(startTimesec).tm_wday] + '요일'
                start = '%s %s %s' % (startDate, wday, startTime)
            else:
                start = ''
            relsec = cont.get('relativeTimeSeconds')
            if relsec:
                relsec = round(relsec)
                if 0<relsec<durationsec:
                    remainsec = durationsec - relsec
                elif relsec < 0:
                    remainsec = -relsec
                else:
                    remainsec = relsec
                remain = '%02d:%02d:%02d' % (remainsec//60//60%24, remainsec//60%60, remainsec%60)
                if remainsec//60//60//24 > 0:
                    remain = '%dday%s ' % (remainsec//60//60//24, '' if remainsec//60//60//24 == 1 else 's') + remain
            else:
                remain = ''
            conList.append((name,start,duration,phase,remain,startTimesec))
    #print(conList)
    return conList

def CFUserInfo(handle):
    try:
        plainCode = requests.get("https://codeforces.com/api/user.info?handles=" + handle,timeout = 5)
        js = json.loads(plainCode.text)
    except:
        return "Timeout"
    if js.get('status') == 'OK':
        result = js.get('result')[0]
    else:
        return js.get('comment')
    handle = result.get('handle')
    rank = result.get('rank','None')
    rating = result.get('rating')
    if rating :
        rating = str(rating)
    else:
        rating = 'None'
    return '[Codeforces] ' + handle + ' : ' + rank + ' - ' + rating

def CFRatingChange(handle,preList):
    url = 'http://codeforces.com/api/user.rating?handle='+handle
    try:
        plainCode = requests.get(url)
        rjson = json.loads(plainCode.text)
    except:
        return False
    if rjson['status']=='OK':
        newChangeList = []
        result = rjson.get('result')
        for x in result:
            if not x.get('contestId') in preList:
                newChangeList.append(x)
        return newChangeList
    else:
        return False
        

def InitCFChangeList(handle):
    url = 'http://codeforces.com/api/user.rating?handle='+handle
    try:
        plainCode = requests.get(url)
        rjson = json.loads(plainCode.text)
    except:
        return False
    if rjson['status'] == 'OK':
        result = rjson.get('result')
        List = []
        for x in result:
            List.append(x.get('contestId'))
        return List
    else:
        return False
