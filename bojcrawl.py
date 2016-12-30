import requests
from bs4 import BeautifulSoup
import re

class BOJCrawler:
    address = 'https://www.acmicpc.net/'
    short_address = 'https://boj.kr/'

    def get_problem_title(self, num):
        try:
            plainCode = requests.get(self.address + 'problem/' + str(num), timeout = 5)
            soup = BeautifulSoup(plainCode.text, 'html.parser')
            title = soup.select('head > title')[0].string
            if title == 'Baekjoon Online Judge':
                return False
            else:
                return title
        except requests.Timeout:
            raise
        except:
            return False

    def command(self, text):
        result = []
        if text.isnumeric():
            num = int(text)
            try:
                title = self.get_problem_title(num)
            except requests.Timeout:
                result.append('Timeout')
            if title:
                result.append('%s -> %s%d' % (title, self.short_address, num))
            else:
                result.append('Problem not found')
        return result

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
