class Counter:
    def score(self, phrase):
        sum=0
        for c in phrase.lower():
            if 'a' <= c <= 'z':
                sum += ord(c) - ord('a') + 1
            elif '0' <= c <= '9':
                sum += ord(c) - ord('0')
            elif 65345 <= ord(c) <= 65370:
                sum += ord(c) - 65344
            elif 65313 <= ord(c) <= 65338:
                sum += ord(c) - 65312
        if sum == 0:
            return 0
        elif sum%100 == 0:
            return 100
        else:
            return sum % 100

    def valid_phrase(self, phrase):
        for c in phrase.lower():
            if not ('a' <= c <= 'z'\
                    or '0' <= c <= '9'\
                    or 65345<=ord(c)<=65370\
                    or 65313<=ord(c)<=65338\
                    or (c in " \'\"-?!.,/")):
                return False
        return True

    def command(self, text):
        if text == None:
            return []
        result = []
        if self.valid_phrase(text):
            score = self.score(text)
            if score == 100:
                result.append("'%s'은(는) %d점짜리 입니다" % (text, score))
            else:
                result.append("'%s'은(는) %d점" % (text, score))
        else:
            result.append('적절하지 않은 영단어입니다')
        return result

