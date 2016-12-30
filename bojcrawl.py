import requests
from bs4 import BeautifulSoup
import re

class BOJCrawler:
    ADDRESS = 'https://www.acmicpc.net/'
    SHORT_ADDRESS = 'https://boj.kr/'

    def get_problem_title(self, num):
        try:
            plain_code = requests.get(self.ADDRESS + 'problem/' + str(num), timeout=5)
            soup = BeautifulSoup(plain_code.text, 'html.parser')
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
        try:
            result = []
            if text.isnumeric():
                num = int(text)
                title = self.get_problem_title(num)
                if title:
                    result.append('%s -> %s%d' % (title, self.SHORT_ADDRESS, num))
                else:
                    result.append('Problem not found')
            return result
        except requests.Timeout:
            return ['Timeout']

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
