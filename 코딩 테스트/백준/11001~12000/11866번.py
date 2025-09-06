import sys
from collections import deque

# input = sys.stdin.readline

n, k = map(int, input().split())
queue = deque()

for i in range(1, n+1):
    queue.append(i)
    
order_list = []
count = 1
    
while len(queue) >= 1:
    if count != k:
        queue.rotate(-1)
        count += 1
    else:
        num = queue.popleft()
        order_list.append(num)
        count = 1

result = ", ".join(map(str, order_list))
print(f"<{result}>")