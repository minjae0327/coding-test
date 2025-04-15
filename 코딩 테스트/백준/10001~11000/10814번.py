import sys
import heapq

input = sys.stdin.readline

n = int(input())
queue = []

for i in range(n):
    age, name = input().split()
    age = int(age)
    
    heapq.heappush(queue, (age, i, name))
    
while queue:
    age, _, name = heapq.heappop(queue)
    print(age, name)
