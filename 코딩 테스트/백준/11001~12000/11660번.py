# backjoon
import sys

input = sys.stdin.readline

n, m = map(int, input().split())

table = [list(map(int, input().split())) for _ in range(n)]
coords = [list(map(int, input().split())) for _ in range(m)]

dp = [[0 for _ in range(n)] for _ in range(n)]

for i in range(n):
    for j in range(n):
        dp[i][j] = table[i][j]
        if i > 0:
            dp[i][j] += dp[i-1][j]
        if j > 0:
            dp[i][j] += dp[i][j-1]
        if i > 0 and j > 0:
            dp[i][j] -= dp[i-1][j-1]
            
def get_sum(x1, y1, x2, y2):
    result = dp[x2][y2]
    if x1 > 0:
        result -= dp[x1-1][y2]
    if y1 > 0:
        result -= dp[x2][y1-1]
    if x1 > 0 and y1 > 0:
        result += dp[x1-1][y1-1]
    return result

                
for coord in coords:
    x1, y1, x2, y2 = coord[0]-1, coord[1]-1, coord[2]-1, coord[3]-1
    
    print(get_sum(x1,y1,x2,y2))