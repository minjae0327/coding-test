# backjoon
import sys
from collections import deque

input = sys.stdin.readline

n, m = map(int, input().split())
land = []

for _ in range(n):
    land.append(list(map(int, input().split())))

def find_position(matrix):
    for i, row in enumerate(matrix):
        if 2 in row:
            return (i, row.index(2))
        
def find_wastedland(land, dp, weighted_map):
    for x, row in enumerate(land):
        for y, num in enumerate(row):
            if dp[x][y] == False and land[x][y] != 0:
                weighted_map[x][y] = -1

dp = [[False for _ in range(m)] for _ in range(n)]
weighted_map = [[0 for _ in range(m)] for _ in range(n)]

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
weight = 0

start_x, start_y = find_position(land)

have_to_visit = deque()
have_to_visit.append((start_x, start_y, weight))
dp[start_x][start_y] = True

while have_to_visit:
    x, y, weight = have_to_visit.popleft()
    weighted_map[x][y] = weight
    
    for i in range(4):
        nx, ny = x + dx[i] ,y + dy[i]
        if 0 <= nx < n and 0 <= ny < m:
            if (dp[nx][ny] == False) and (land[nx][ny] != 0):
                have_to_visit.append((nx, ny, weight + 1))
                dp[nx][ny] = True

find_wastedland(land, dp, weighted_map)
                
for row in weighted_map:
    print(*row)