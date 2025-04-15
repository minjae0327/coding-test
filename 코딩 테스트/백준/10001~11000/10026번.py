import sys
from collections import deque

input = sys.stdin.readline

n = int(input())
rgbs = [list(input().strip()) for _ in range(n)]

area1 = 0
area2 = 0

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def bfs(i, j, color, visited):
    have_to_visit = deque()
    have_to_visit.append((i, j))
    visited[i][j] = True
    
    while have_to_visit:
        x, y = have_to_visit.popleft()
        
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            
            if 0 <= nx < n and 0 <= ny < n:
                if rgbs[nx][ny] in color and not visited[nx][ny]:
                    visited[nx][ny] = True
                    have_to_visit.append((nx, ny))

for color in ['R', 'G', 'B']:
    visited = [[False]*n for _ in range(n)]
    have_to_visit = deque()
    
    for i in range(n):
        for j in range(n):
            if rgbs[i][j] in color and not visited[i][j]:
                bfs(i, j, color, visited)
                area1 += 1

for color in [['R', 'G'], 'B']:
    visited = [[False]*n for _ in range(n)]
    have_to_visit = deque()
    
    for i in range(n):
        for j in range(n):
            if rgbs[i][j] in color and not visited[i][j]:
                bfs(i, j, color, visited)
                area2 += 1

print(area1, area2)