import heapq

n = int(input())

heap = []

for _ in range(n):
    numbers = map(int, input().split())
    
    for num in numbers:
        if len(heap) != n:
            heapq.heappush(heap, -num)
        else:
            comp = heapq.heappop(heap) * -1
            if comp < num:
                heapq.heappush(heap, -num)
            else:
                heapq.heappush(heap, -comp)
            
result = heapq.heappop(heap)

print(int(result) * -1)