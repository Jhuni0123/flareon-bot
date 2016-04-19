import requests
from bs4 import BeautifulSoup
from time import sleep
import re

def MakeNameDic(List):
    dic = {}
    dic['원'] = 'KRW'
    dic['엔'] = 'JPY'
    dic['달러'] = 'USD'
    dic['파운드'] = 'GBP'
    dic['위안'] = 'CNY'
    dic['유로'] = 'EUR'
    dic['남아공'] = 'ZAR'
    dic['유럽'] = 'EUR'
    
    for i in range(1,len(List)):
        name = List[i][0]
        parse = re.match(r'(\S+)(\s*\S*)\s+([A-Z]{3})\s*(\S*)$',name)
        if parse:
            ctry = parse.group(1)+parse.group(2)
            simbol = parse.group(3)
            dic[ctry]=simbol
            dic[simbol]=simbol
    return dic

def UpdateExDic(List,dic):
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

def ExchangeCrawl():
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

def WriteTable(List):
    strlist=[]
    for x in List:
        strlist.append('|'.join(x))
    string = '\n'.join(strlist)
    f=open("exchange_table.txt",mode = 'w',encoding = 'utf8')
    f.write(string)
    f.close()


def Exmsg(contents,exDic,nameDic):
    contents = contents.strip(' \t\n\r')
    parse = re.match(r'(\d*)\s*(\S+)(?:\s*->\s*(\S+)\s*)?$',contents)
    if parse:
        num1 = parse.group(1)
        name1 = parse.group(2)
        name2 = parse.group(3)
                                
        if name1 == 'info' or name1 == '정보':
            return exDic['info']
        if name1 == 'help' or name1 == '도움':
            return 'ex)!환율 [숫자] <통화명> [-> <통화명>]'
                                    
        if name1:
            name1 = nameDic.get(name1.upper())
                                    
        if name2:
            name2 = nameDic.get(name2.upper())
        else:
            name2 = 'KRW'
                                    
        if name1 and name2:
            if num1 == '':
                if exDic[name1][1]:
                    num1 = 100
                else:
                    num1 = 1
            else:
                num1 = int(num1)
                                    
            m1=exDic[name1][0]
            m2=exDic[name2][0] 
            if exDic[name1][1]:
                m1 = m1/100.0
            if exDic[name2][1]:
                m2 = m2/100.0
                                    
            return '%d %s = %.2f %s' % (num1,name1,num1*m1/m2,name2)
        
        else:
            return 'Not Found'
    else:
        return 'ex)!환율 [숫자] <통화명> [-> <통화명>]'
