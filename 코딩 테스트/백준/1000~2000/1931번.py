# backjoon
import sys
# from collections import deque
from collections import defaultdict

input = sys.stdin.readline

# n, m = map(int, input().split())

N = int(input())
schedules = [list(map(int, input().split())) for _ in range(N)]

schedules.sort(key=lambda x: (x[1], x[0]))

teams = 0
time = 0

for start, end in schedules:
    if start >= time:
        time = end
        teams += 1
        
print(teams)