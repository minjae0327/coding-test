# backjoon
import sys
from collections import deque
# from collections import defaultdict

input = sys.stdin.readline

m, n = map(int, input().split())

# N = int(input())
tomatoes = [list(map(int, input().split())) for _ in range(n)]

coordinates = []
days = 0

for x, row in enumerate(tomatoes):
    for y, num in enumerate(row):
        if num == 1:
            coordinates.append([x, y])
            break
        
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

have_to_visit = deque()
for x ,coord in enumerate(coordinates):
    have_to_visit.append((coord[0], coord[1], days))

while have_to_visit:
    x, y, days = have_to_visit.popleft()
    tomatoes[x][y] = 1
    
    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]
        
        if 0 <= nx < n and 0 <= ny < m:
            if tomatoes[nx][ny] == 0:
                have_to_visit.append((nx, ny, days + 1))
                

def check_waste():
    for x, row in enumerate(tomatoes):
        for y, num in enumerate(row):
            if num == 0:
                return True
                
if check_waste():
    print(-1)
else:
    print(days)