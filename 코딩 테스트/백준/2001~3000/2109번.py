import heapq

n = int(input())

if n == 0:
    print(0)
    exit()

speeches = [list(map(int, input().split())) for _ in range(n)]

speeches.sort(key=lambda x : x[1])
max_heap = []
heapq.heappush(max_heap, (speeches[0][0], speeches[0][1]))

for i in range(1, n):
    speech = speeches[i]
        
    if len(max_heap) < speech[1]:
        heapq.heappush(max_heap, (speech[0], speech[1]))
    else:
        if speech[0] > max_heap[0][0]:
            heapq.heappop(max_heap)
            heapq.heappush(max_heap, (speech[0], speech[1]))
        
result = 0

for speech in max_heap:
    result += speech[0]
    
print(result)