# backjoon
from collections import deque

def bfs(maps, x, y):
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    
    have_to_visit = deque()
    have_to_visit.append((x, y))
    
    maps[x][y] = "0"
    count = 1
    
    while have_to_visit:
        x, y = have_to_visit.popleft()
            
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            
            if 0 <= nx < len(maps) and 0 <= ny < len(maps[0]):
                if maps[nx][ny] == "1":
                    have_to_visit.append((nx, ny))
                    maps[nx][ny] = "0"
                    count += 1
                       
    return count

N = int(input())
maps = []

for _ in range(N):
    _maps = list(input().strip())
    maps.append(_maps)
    
villages = 0
dict_villages = {}
    
for i in range(N):
    for j in range(N):
        if maps[i][j] == "1":
            villages += 1
            dict_villages[villages] = bfs(maps, i, j)
            
village_sizes = sorted(dict_villages.values())

print(villages)
for size in village_sizes:
    print(size)