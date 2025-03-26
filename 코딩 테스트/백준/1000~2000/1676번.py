import math

N = int(input())
a = str(math.factorial(N))

count = 0

for i in range(len(a)-1, -1, -1):
    if a[i] == '0':
        count += 1
    elif a[i] != 0:
        print(count)
        break