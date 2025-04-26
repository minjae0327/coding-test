import sys

input = sys.stdin.readline

n = int(input())
m = int(input())

INF = float('inf')
dist = [[INF] * n for _ in range(n)]
for i in range(n):
    dist[i][i] = 0

for _ in range(m):
    start, end, weight = map(int, input().split())
    if weight < dist[start - 1][end - 1]:
        dist[start - 1][end - 1] = weight

# Floyd-Warshall
for k in range(n):
    for i in range(n):
        for j in range(n):
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

for i in range(n):
    for j in range(n):
        if dist[i][j] == INF:
            print(0, end=' ')
        else:
            print(dist[i][j], end=' ')
    print()
