# -*- coding: utf-8 -*-

import re


class FibCalculator:
    def __init__(self):
        self.MAX_N = 256
        self.fib = [0,1]
        self.fib_minus = [1,-1]
        for _ in range(self.MAX_N):
            self.fib.append(self.fib[-1] + self.fib[-2])
            self.fib_minus.append(self.fib_minus[-2] - self.fib_minus[-1])

    # proper number of chickens for n people
    # use Zeckendorf’s Theorem
    def chibonacci(self, n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        l=0
        r=101
        while l<r:
            k=(l+r)//2
            if self.fib[k] <= n:
                l=k+1
            else:
                r=k
        return self.fib[r-2] + self.chibonacci(n-self.fib[r-1])

    def fibonacci(self, n):
        if abs(n) > self.MAX_N:
            return None
        elif n < 0:
            return self.fib_minus[-n]
        else:
            return self.fib[n]

    def chicken_command(self, text):
        if text == None:
            return []
        try:
            result = []
            text = text.strip()
            match = re.fullmatch('(b?\d+)\s*명?',text)
            digits = match.group(1)
            isbin = False
            if digits.startswith('b'):
                isbin = True
                num = int('0' + digits, 2)
            else:
                num = int(digits)

            if num == 1:
                result.append('1인1닭은 진리입니다')
            elif num == 2:
                result.append('계산상 1마리지만 1인1닭도 좋습니다')
            elif num >= 573147844013817084101:
                result.append('필요한 치킨이 너무 많아 셀 수 없습니다')
            else:
                chicken = self.chibonacci(num)
                result.append('%s명에게는 %s마리의 치킨이 적절합니다'\
                        % (bin(num) if isbin else str(num),\
                                bin(chicken) if isbin else str(chicken)))

            if num == 12117:
                result.append('gs12117에게는 0.3마리의 치킨이면 충분합니다')
        except:
            return ['Incorrect input']
        else:
            return result

    def fib_command(self, text):
        if text == None:
            return []
        result = []
        text = text.strip()
        try:
            num = int(text)
        except ValueError:
            result.append('Incorret input')
        else:
            res = self.fibonacci(num)
            if res == None:
                result.append('result is to big')
            else:
                result.append('[fib] ' + str(res))
        return result
