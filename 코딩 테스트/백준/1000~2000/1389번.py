import sys
from collections import defaultdict, deque

graph = defaultdict(list)

input = sys.stdin.readline

n, m = map(int, input().split())

for i in range(1, n+1):
    graph[i] = []

def add_edge(start, end):
    graph[start].append(end)
    graph[end].append(start)

for i in range(m):
    start, end = map(int, input().split())
    add_edge(start, end)
    
def bfs(graph, start):
    result = 0

    visited = set()
    have_to_visit = deque()
    
    have_to_visit.append((start, 0))
    visited.add(start)
    
    while have_to_visit:
        friend, bridge = have_to_visit.popleft()
        
        for man in graph[friend]:
            if man not in visited:
                have_to_visit.append((man, bridge + 1))
                visited.add(man)
                result += bridge + 1
            
    return result

result = [bfs(graph,i) for i in range(1, n+1)]
print(result.index(min(result)) + 1)
