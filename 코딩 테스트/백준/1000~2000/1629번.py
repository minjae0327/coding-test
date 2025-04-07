import sys

input = sys.stdin.readline

a, b, c = map(int, input().split())

def moduler_exponentitaion(a, b, c):
    if b == 0:
        return 1
    elif b % 2 == 0:
        temp = moduler_exponentitaion(a, b // 2, c)
        return (temp * temp) % c
    else:
        return (a * moduler_exponentitaion(a, b-1, c)) % c
    
print(moduler_exponentitaion(a, b, c))