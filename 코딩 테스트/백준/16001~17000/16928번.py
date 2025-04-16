import sys
from collections import deque, defaultdict

input = sys.stdin.readline

n, m = map(int, input().split())

ladders = defaultdict(int)
snakes = defaultdict(int)

for _ in range(n):
    a, b = map(int, input().split())
    ladders[a] = b
    
for _ in range(m):
    a, b = map(int, input().split())
    snakes[a] = b

def bfs(start, count):
    visited = [False] * 101
    have_to_visit = deque()
    have_to_visit.append((start, count))
    visited[1] = True
    
    while have_to_visit:
        point, count = have_to_visit.popleft()
        
        if point == 100:
            return count
          
        count += 1
        
        for i in range(1, 6+1):
            potential_point = point + i
            
            if 0 < potential_point <= 100 and not visited[potential_point]:
                if potential_point in ladders:
                    potential_point = ladders[potential_point]
                elif potential_point in snakes:
                    potential_point = snakes[potential_point]
                    
                if not visited[potential_point]:
                    have_to_visit.append((potential_point, count))
                    visited[potential_point] = True
                

start = 1
count = 0

print(bfs(start, count))