import heapq

N = int(input())
schedules = [list(map(int, input().split())) for _ in range(N)]

schedules.sort(key=lambda x: (x[0], x[1]))

heap = []
heapq.heappush(heap, schedules[0][1])

for i in range(1, N):
    start, end = schedules[i]
    first_classtime = heap[0]
    
    if first_classtime <= start:
        heapq.heappop(heap)
        heapq.heappush(heap, end)
    else:
        heapq.heappush(heap, end)
    
        
print(len(heap))