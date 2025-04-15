import sys
from collections import deque

input = sys.stdin.readline

n, m, h = map(int, input().split())

tomatoes = [[] for _ in range(h)]

for k in range(h):
    for _ in range(m):
        row = list(map(int, input().split()))
        tomatoes[k].append(row)

have_to_visit = deque()
days = 0

dx = [-1, 1, 0, 0, 0, 0]
dy = [0, 0, -1, 1, 0, 0]
dz = [0, 0, 0, 0, -1, 1]

#익은 토마토 추가
for z in range(h):
    for x in range(m):
        for y in range(n):
            if tomatoes[z][x][y] == 1:
                have_to_visit.append((x, y, z, 0))

#BFS
while have_to_visit:
    x, y, z, days = have_to_visit.popleft()
    
    for i in range(6):
        nx = x + dx[i]
        ny = y + dy[i]
        nz = z + dz[i]
        
        if 0 <= nx < m and 0 <= ny < n and 0 <= nz < h:
            if tomatoes[nz][nx][ny] == 0:
                tomatoes[nz][nx][ny] = 1
                have_to_visit.append((nx, ny, nz, days + 1))
                
def check_waste():
    for z in range(h):
        for x in range(m):
            for y in range(n):
                if tomatoes[z][x][y] == 0:
                    return True
                
    return False
                
if check_waste():
    print(-1)
else:
    print(days)