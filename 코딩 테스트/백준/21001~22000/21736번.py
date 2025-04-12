# backjoon
from collections import deque

def bfs(maps, x, y):
    meeted = 0
    
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    
    visited = set()
    have_to_visit = deque()
    
    have_to_visit.append((x, y))
    
    while have_to_visit:
        x, y = have_to_visit.popleft()
            
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            
            if 0 <= nx < len(maps) and 0 <= ny < len(maps[0]):
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    if maps[nx][ny] == "X":
                        continue
                    if maps[nx][ny] == "P":
                        meeted += 1
                    have_to_visit.append((nx, ny))
                    
    meeted = meeted if meeted > 0 else "TT"  
    return meeted

n, m = map(int, input().split())
maps = []

for i in range(n):
    row = input().strip()
    row_list = list(row)
    maps.append(row_list)
    
    if "I" in row_list:
        j = row_list.index("I")
        I_position = (i, j)

print(bfs(maps, I_position[0], I_position[1]))