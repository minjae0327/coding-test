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
    
def bfs(s):
    global order
    visited[s] = order
    have_to_visit = deque()
    have_to_visit.append(s)
    order += 1
    
    while have_to_visit:
        node = have_to_visit.popleft()
        for neighbor in dist[node]:
            if visited[neighbor] == 0:
                visited[neighbor] = order
                order += 1
                have_to_visit.append(neighbor)
            
bfs(start)

for i in range(1, n+1):
    print(visited[i])