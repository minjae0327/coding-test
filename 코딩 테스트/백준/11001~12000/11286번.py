import heapq
import sys

input = sys.stdin.readline

n = int(input())
queue = []

for _ in range(n):
    num = int(input())
    if num == 0:
        if len(queue) == 0:
            print("0")
        else:
            print(heapq.heappop(queue)[1])
    else:
        heapq.heappush(queue, (abs(num), num))
