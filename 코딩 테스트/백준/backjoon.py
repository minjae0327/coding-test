import heapq
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
            
    
    def display(self):
        for vertex in self.graph:
            print(f"{vertex}: {self.graph[vertex]}")
            
            
    def bfs(self, start):
        visited = set()
        visit_order = []
        have_to_visit = deque()
        have_to_visit.append(start)
        visited.add(start)
        
        while have_to_visit:
            vertex = have_to_visit.popleft()
            visit_order.append(vertex)
            
            for node in self.graph[vertex]:
                neighbor = node[0]
                
                if neighbor not in visited:
                    have_to_visit.append(neighbor)
                    visited.add(neighbor)
                    
        return visit_order
    
    
    def dfs(self, start):
        visited = set()
        visit_order = []
        have_to_visit = []
        have_to_visit.append(start)
        visited.add(start)
        
        while have_to_visit:
            vertex = have_to_visit.pop()
            visit_order.append(vertex)
            
            # 인접 노드를 역순으로 추가
            for node in reversed(self.graph.get(vertex, [])):
                neighbor = node[0]
                if neighbor not in visited:
                    have_to_visit.append(neighbor)
                    visited.add(neighbor)
                    
        return visit_order
        
    
    def display(self):
        for vertex in self.graph:
            print(f"{vertex}: {self.graph[vertex]}")


graph = Graph()

# vertexs, edges, start = map(int, input().split(" "))
vertexs, edges, start = 4, 5, 1

for _ in range(edges):
    _start, _end = map(int, input().split(" "))
    graph.add_edge(_start, _end)
    
graph.dfs(start)
graph.bfs(start)

        