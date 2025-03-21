from collections import deque

class Graph:
    def __init__(self):
        self.graph = {}
        
    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []
            
    def add_edge(self, start, end, weight=None, directed=False):
        if start not in self.graph:
            self.add_vertex(start)
        if end not in self.graph:
            self.add_vertex(end)
           
        self.graph[start].append([end, weight])
        if not directed:
            self.graph[end].append([start, weight])
            
    def bfs(self, start):
        visit_order = []
        visited = set()
        have_to_visit = deque()
        have_to_visit.append(start)
        
        while have_to_visit:
            vertex = have_to_visit.popleft()
            if vertex not in visited:
                visit_order.append(vertex)
                visited.add(vertex)
            
            for node in sorted(self.graph.get(vertex, [])):
                neighbor = node[0]
                if neighbor not in visited:
                    have_to_visit.append(neighbor)
                    
        return visit_order
    
    def dfs(self, start):
        visit_order = []
        visited = set()
        have_to_visit = [start]
        
        while have_to_visit:
            vertex = have_to_visit.pop()
            if vertex not in visited:
                visit_order.append(vertex)
                visited.add(vertex)
            
            # 인접 노드를 역순으로 추가하여 작은 번호가 먼저 방문되도록 함
            for node in reversed(sorted(self.graph.get(vertex, []))):
                neighbor = node[0]
                if neighbor not in visited:
                    have_to_visit.append(neighbor)
                    
        return visit_order
        
    def display(self):
        for vertex in self.graph:
            print(f"{vertex}: {self.graph[vertex]}")

graph = Graph()
n, m, start = map(int, input().split())
for _ in range(m):
    _start, _end = map(int, input().split())
    graph.add_edge(_start, _end)
    
print(" ".join(map(str, graph.dfs(start))))
print(" ".join(map(str, graph.bfs(start))))
