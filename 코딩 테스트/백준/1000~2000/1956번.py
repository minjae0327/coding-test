import sys

input = sys.stdin.readline

n, m = map(int, input().split())

INF = float("inf")

maps = [[INF] * n for _ in range(n)]

for i in range(n):
    maps[i][i] = 0

for i in range(m):
    start, end, weight = map(int, input().split())
    if weight < maps[start-1][end-1]:
        maps[start-1][end-1] = weight
        
#floya-warshall
for k in range(n):
    for i in range(n):
        for j in range(n):
            maps[i][j] = min(maps[i][j], maps[i][k] + maps[k][j])
            
result = INF

for i in range(n):
    for j in range(n):
        if i == j:
            continue
        a = maps[i][j]
        b = maps[j][i]
        
        if (a != INF and b != INF) and a + b < result:
            result = a + b

if result == INF:
    print(-1)
else:
    print(result)