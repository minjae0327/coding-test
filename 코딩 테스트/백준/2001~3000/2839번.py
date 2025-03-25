from collections import defaultdict
#BFS
N = int(input())   

dict = defaultdict(set)
loc = 0
dict[loc].add(0)

if (N == 4):
    print(-1)
elif N % 5 == 0:
    print(N // 5)
else:
    while True:
        for d in dict[loc]:
            dict[loc + 1].add(d + 3)
            dict[loc + 1].add(d + 5)

        if N in dict[loc + 1]:
            print(loc + 1)
            break
        
        if N < min(dict[loc + 1]):
            print(-1)
            break

        loc += 1
        
# Greedy
N = int(input())

cnt = 0
while N >= 0:
    if N % 5 == 0:
        cnt += N // 5
        print(cnt)
        break
    N -= 3
    cnt += 1
else:
    print(-1)