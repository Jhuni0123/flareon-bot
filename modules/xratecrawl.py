# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
import re


class XRateCrawler:
    help_msg = 'ex)!환율 [숫자] <통화명> [-> <통화명>]'

    def __init__(self):
        self.xr_list = []
        self.name_to_sym = {}
        self.xrate = {}
        self.update()

    def update(self):
        self.xr_list = self.crawl_xrate()
        print(datetime.now())
        print(len(self.xr_list))
        self.name_to_sym = self.make_name_to_sym(self.xr_list)
        self.xrate = self.update_xrate(self.xr_list, self.xrate)

    def make_name_to_sym(self, List):
        dic = {
                '원': 'KRW',
                '엔': 'JPY',
                '달러': 'USD',
                '파운드': 'GBP',
                '위안': 'CNY',
                '유로': 'EUR',
                '남아공': 'ZAR'
                }
        for i in range(1,len(List)):
            name = List[i][0]
            parse = re.match(r'(\S+)(\s*\S*)\s+([A-Z]{3})\s*(\S*)$',name)
            if parse:
                ctry = parse.group(1)+parse.group(2)
                simbol = parse.group(3)
                dic[ctry]=simbol
                dic[simbol]=simbol
        return dic

    def update_xrate(self, List,dic):
        try:
            dic['info'] = List[0][1]
            for i in range(1,len(List)):
                name = List[i][0]
                parse = re.match(r'(\S+)(\s*\S*)\s+([A-Z]{3})\s*(\S*)$',name)
                if parse:
                    ctry = parse.group(1)+parse.group(2)
                    simbol = parse.group(3)
                    isHundred = not parse.group(4)==''
                    dic[simbol]=(float(List[i][1].replace(',','')),isHundred)
            return dic
        except Exception as e:
            print(datetime.now())
            print(e)
            print(List)
            print(dic)
            return dic

    def crawl_xrate(self):
        List = []
        try:
            sourceHtml = requests.get("http://info.finance.naver.com/marketindex/?tabSel=exchange#tab_section",timeout=5)
        except:
            return []
        sourceText = sourceHtml.text
        soup = BeautifulSoup(sourceText, 'html.parser')
        info = soup.select('div.exchange_info')[0].text.strip('\n ').replace('\n','/')
        List.append(('info',info))
        try:
            sourceHtml = requests.get("http://info.finance.naver.com/marketindex/exchangeList.nhn",timeout=5)
        except:
            return []
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

    def WriteTable(self, List):
        strlist=[]
        for x in List:
            strlist.append('|'.join(x))
        string = '\n'.join(strlist)
        f=open("exchange_table.txt",mode = 'w',encoding = 'utf8')
        f.write(string)
        f.close()


    def command(self, text):
        if text == None:
            return [self.help_msg]
        else:
            text = text.strip(' \t\n\r')
            parse = re.match(r'(\d*(?:(?:\.\d+)?|(?:e(?:\+|-)?\d+)?))\s*([^\s\d>-]+)(?:\s*->\s*([^\s\d]+)\s*)?$',text)
            if parse:
                num1 = parse.group(1)
                name1 = parse.group(2)
                name2 = parse.group(3)

                if name1 == 'info' or name1 == '정보':
                    return [self.xrate['info']]
                if name1 == 'help' or name1 == '도움':
                    return [self.help_msg]
                if name1:
                    name1 = self.name_to_sym.get(name1.upper())
                if name2:
                    name2 = self.name_to_sym.get(name2.upper())
                else:
                    name2 = 'KRW'
                if name1 and name2:
                    if num1 == '':
                        if self.xrate[name1][1]:
                            num1 = 100
                        else:
                            num1 = 1
                    else:
                        num1 = float(num1)
                    m1=self.xrate[name1][0]
                    m2=self.xrate[name2][0]
                    if self.xrate[name1][1]:
                        m1 = m1/100.0
                    if self.xrate[name2][1]:
                        m2 = m2/100.0
                    return ['%g %s = %.2f %s' % (num1,name1,num1*m1/m2,name2)]
                else:
                    return ['Not Found']
            else:
                return [self.help_msg]
