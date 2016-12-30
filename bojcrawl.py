import requests
from bs4 import BeautifulSoup

class BOJCrawler:
    ADDRESS = 'https://www.acmicpc.net/'
    SHORT_ADDRESS = 'https://boj.kr/'

    def get_problem_title(self, num):
        try:
            plain_code = requests.get(self.ADDRESS + 'problem/' + str(num), timeout=5)
            soup = BeautifulSoup(plain_code.text, 'html.parser')
            title = soup.select('head > title')[0].string
        except requests.Timeout:
            raise
        except:
            return False
        else:
            if title == 'Baekjoon Online Judge':
                return False
            else:
                return title

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
        except requests.Timeout:
            return ['Timeout']
        else:
            return result
