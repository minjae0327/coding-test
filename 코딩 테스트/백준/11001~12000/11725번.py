# backjoon
import sys
from collections import deque
from collections import defaultdict

input = sys.stdin.readline

n = int(input())
edges = [list(map(int, input().split())) for _ in range(n-1)]

def add_edge(start, end):
    graph[start].append(end)
    graph[end].append(start)

graph = defaultdict(list)
visited_graph = defaultdict(int)
visited_graph[1] = 0

for edge in edges:
    add_edge(edge[0], edge[1])
    
visited = set()

have_to_visit = deque()
have_to_visit.append((1, 0))

while have_to_visit:
    node, parent = have_to_visit.popleft()
    
    visited.add(node)
    visited_graph[node] = parent
    
    for child in graph[node]:
        if child not in visited:
            have_to_visit.appendleft((child, node))
            
for key in sorted(visited_graph.keys()):
    if key != 1:
        print(visited_graph[key])