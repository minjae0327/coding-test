import sys
import heapq

input = sys.stdin.readline

max_size = int(input())
heap = []

for i in range(max_size):
    num = int(input())
    if num == 0:
        if len(heap) == 0:
            print(0)
        else:
            print(heapq.heappop(heap)[1])
    else:
        heapq.heappush(heap, [-num, num])