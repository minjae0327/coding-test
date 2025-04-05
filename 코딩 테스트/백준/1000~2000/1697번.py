# backjoon
import sys
from collections import deque

input = sys.stdin.readline

N, K = map(int, input().split())

visited = [False] * 100001
visited[N] = True

have_to_visit = deque()
have_to_visit.append((N, 0))

while have_to_visit:
    current, cost = have_to_visit.popleft()
    
    if current == K:
        print(cost)
        break

    for next_pos in (current - 1, current + 1, current * 2):
        if 0 <= next_pos <= 100000 and not visited[next_pos]:
            visited[next_pos] = True
            have_to_visit.append((next_pos, cost + 1))