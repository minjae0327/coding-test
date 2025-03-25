# backjoon
from collections import deque

def bfs(maps, x, y):
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    
    have_to_visit = deque()
    have_to_visit.append((x, y))
    
    maps[x][y] = "0"
    
    while have_to_visit:
        x, y = have_to_visit.popleft()
            
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            
            if 0 <= nx < len(maps) and 0 <= ny < len(maps[0]):
                if maps[nx][ny] == "1":
                    have_to_visit.append((nx, ny))
                    maps[nx][ny] = "0"
                    
    return maps

T = int(input())
maps = []

for _ in range(T):
    M, N, K = map(int, input().split(" "))
    maps = [['0' for _ in range(N)] for _ in range(M)]
    for _ in range(K): 
        x, y = map(int, input().split(" "))
        maps[x][y] = '1'
    
    villages = 0
        
    for i in range(M):
        for j in range(N):
            if maps[i][j] == "1":
                villages += 1
                maps = bfs(maps, i, j)

    print(villages)