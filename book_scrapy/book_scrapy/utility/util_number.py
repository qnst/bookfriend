#coding:utf-8
#任意进制转换

def radix(src,n):
    assert 2<=n<=36
    loop = '0123456789abcdefghijklmnopqrstuvwxyz'
    loop=loop[:n]
    a = []
    while src != 0:
        a.append(loop[src%n])
        src = src/n
    a.reverse()
    return ''.join(a)