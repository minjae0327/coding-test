# backjoon
import heapq
import sys
input = sys.stdin.readline  # 더 빠른 입력 처리

n = int(input())

queue = []

for _ in range(n):
    num = int(input())
    if num > 0:
        heapq.heappush(queue, num)
    else:
        if len(queue) == 0:
            print(0)
        else:
            print(heapq.heappop(queue))
