# backjoon
import sys
from collections import deque

input = sys.stdin.readline

N, K = map(int, input().split())

MAX = 100001
visited = [0] * MAX
count = [0] * MAX

have_to_visit = deque()
have_to_visit.append(N)
visited[N] = 1
count[N] = 1

while have_to_visit:
    current = have_to_visit.popleft()

    for next_pos in (current - 1, current + 1, current * 2):
        if 0 <= next_pos < MAX:
            if visited[next_pos] == 0:
                visited[next_pos] = visited[current] + 1
                count[next_pos] = count[current]
                have_to_visit.append(next_pos)
            elif visited[next_pos] == visited[current] + 1:
                count[next_pos] += count[current]
                
print(visited[K]-1)
print(count[K])