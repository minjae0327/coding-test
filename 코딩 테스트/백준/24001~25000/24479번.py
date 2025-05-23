import sys
from collections import defaultdict, deque

input = sys.stdin.readline
n, m, start = map(int, input().split())

dist = defaultdict(list)

for _ in range(m):
    u, v = map(int, input().split())
    dist[u].append(v)
    dist[v].append(u)
for i in range(1, n+1):
    dist[i].sort()

visited = [0] * (n+1)
order = 1

def dfs(start):
    global order
    stack = [start]

    while stack:
        node = stack.pop()
        if visited[node] != 0:
            continue
        visited[node] = order
        order += 1
        for neighbor in reversed(dist[node]):
            if visited[neighbor] == 0:
                stack.append(neighbor)

dfs(start)

for i in range(1, n+1):
    print(visited[i])
