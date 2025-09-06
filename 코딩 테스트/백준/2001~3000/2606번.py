from collections import defaultdict, deque

n = int(input())
m = int(input())

graph = defaultdict(list)

for i in range(m):
    start, end = map(int, input().split())
    graph[start].append(end)
    graph[end].append(start)
    
def bfs(graph, start):
    visit_order = []
    visited = set()
    have_to_visit = deque()
    
    visited.add(start)
    have_to_visit.append(start)
    
    while have_to_visit:
        vertex = have_to_visit.popleft()
        visit_order.append(vertex)
        
        for node in graph[vertex]:
            if node not in visited:
                visited.add(node) 
                have_to_visit.append(node)
                
    return visit_order

print(len(bfs(graph, 1)) - 1)