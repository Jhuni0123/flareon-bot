fib=[0,1]
for i in range(2,258):
    fib.append(fib[i-1]+fib[i-2])
    
def Chib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    l=0
    r=101
    while l<r:
        k=(l+r)//2
        if fib[k] <= n:
            l=k+1
        else:
            r=k
    return fib[r-2] + Chib(n-fib[r-1])

def EE(n):
    if n==2:
        return False
    while n>0:
        if n%10 !=2:
            return False
        n=n//10
    return True

def Bi(n):
    if n==0 or n==1:
        return False
    while n>0:
        if n%10 != 0 and n%10 != 1:
            return False
        n = n//10
    return True

def Mkd(n):
    sum = 0
    k=1
    while n>0:
        if n%10 ==1:
           sum = sum+k
        n = n//10
        k=k*2
    return sum

def Mkbi(n):
    ret = ''
    while n>0:
        if n%2 == 1:
            ret = '1' + ret
        else:
            ret = '0' + ret
        n = n//2
    return 'b' + ret
