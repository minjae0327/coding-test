# backjoon
N = int(input())
a = []
for _ in range(N):
    a.append(input())

a = list(set(a))
a.sort(key=lambda x:(len(x), x))

for i in a:
    print(i)