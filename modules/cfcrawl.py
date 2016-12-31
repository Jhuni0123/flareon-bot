# -*- coding: utf-8 -*-

import requests, json
from bs4 import BeautifulSoup
import re, time

class CodeforcesCrawler:
    def contest_list(self):
        wdays = ['월','화','수','목','금','토','일']
        now = round(time.time())

        Dic = self.get_json_api('contest.list')
        if Dic.get('status')=='OK':
            List = Dic.get('result')
        else:
            return [Dic.get('comment')]
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
        result = []
        conlist = sorted(conList, key=lambda con: con[5])
        for con in conlist:
            result.append('[%s] %s | %s | %s | %s' % (con[0],con[1], con[2],con[3],con[4]))
        return result

    def users_info(self, user_handle):
        js = self.get_json_api("user.info?handles=" + user_handle)
        if js.get('status') == 'OK':
            ret = []
            result = js.get('result')
            for user in result:
                user_handle = user.get('handle')
                rank = user.get('rank','None')
                rating = user.get('rating')
                if rating :
                    rating = str(rating)
                else:
                    rating = 'None'
                ret.append('[Codeforces] ' + user_handle + ' : ' + rank + ' - ' + rating)
            return ret
        else:
            return js.get('comment')

    def command(self, text=None):
        try:
            result = []
            if text == None:
                contests = self.contest_list()
                if len(contests) == 0:
                    result.append('No contests yet')
                else:
                    result.extend(contests)
            else:
                text = text.strip()
                info = self.users_info(text)
                result.extend(info)
        except requests.Timeout:
            return ['Timeout']
        else:
            return result

    def get_json_api(self, text):
        plain_code = requests.get('http://codeforces.com/api/' + text, timeout=5)
        res = json.loads(plain_code.text)
        return res

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
