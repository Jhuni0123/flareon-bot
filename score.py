def Score(s):
    sum=0
    for c in s:
        if 'a'<=c<='z':
            sum=sum+ord(c)-96
        elif 'A'<=c<='Z':
            sum=sum+ord(c)-64
        elif 65345<=ord(c)<=65370:
            sum=sum+ord(c)-65344
        elif 65313<=ord(c)<=65338:
            sum=sum+ord(c)-65312
    return sum

def Sent(s):
    for c in s:
        if not ('a' <= c <= 'z' or 'A' <= c <= 'Z' or 65345<=ord(c)<=65370 or 65313<=ord(c)<=65338 or (c in " \'\"-?!.,/")):
            return ''
    return s
