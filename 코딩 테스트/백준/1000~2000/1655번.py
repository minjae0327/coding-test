"""
max heap에는 중간값보다 작은 값이, min_heap에는 중간값보다 큰 값이 들어감

- 규칙 1 (크기 균형): `max_heap`의 크기는 항상 `min_heap`의 크기와 같거나 하나 더 많음
  이렇게 하면 전체 원소의 개수가 홀수일 때나 짝수일 때나 항상 `max_heap`의 루트가 중간값이 됨

- 규칙 2 (값의 순서): `max_heap`의 모든 원소는 `min_heap`의 모든 원소보다 작거나 같아야 합
  즉, `max_heap`의 최댓값 <= `min_heap`의 최솟값이 항상 성립
  만약 이 조건이 깨지면 두 힙의 루트 값을 서로 교환
"""
import heapq

n = int(input())

min_heap = []
max_heap = []
answer = []

for i in range(n):
    num = int(input())
    
    if len(min_heap) == len(max_heap):
        heapq.heappush(max_heap, (-num, num))
    else:
        heapq.heappush(min_heap, (num, num))
        
    if min_heap and max_heap[0][1] > min_heap[0][0]:
        min_num = heapq.heappop(min_heap)[0]
        max_num = heapq.heappop(max_heap)[1]
        heapq.heappush(max_heap, (-min_num, min_num))
        heapq.heappush(min_heap, (max_num, max_num))
        
    answer.append(max_heap[0][1])
    
for num in answer:
    print(num)
