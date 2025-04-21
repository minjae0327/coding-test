import sys
from collections import deque

input = sys.stdin.readline

N, S = map(int, input().split())
arr = list(map(int, input().split()))

count = 0
have_to_visit = deque()
have_to_visit.append((0, 0))
    
while have_to_visit:
    index, num = have_to_visit.popleft()
    
    if index == N:
        if num == S:
            count += 1
        continue
    
    have_to_visit.appendleft((index + 1, num))
    have_to_visit.appendleft((index + 1, num + arr[index]))

if S==0:
    count -= 1
    
print(count)