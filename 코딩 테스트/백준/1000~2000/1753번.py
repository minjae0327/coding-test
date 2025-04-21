import sys
import heapq

input = sys.stdin.readline

v, e = map(int, input().split())
k = int(input())

graph = [[] for _ in range(v+1)]
for _ in range(e):
    start, end, weight = map(int, input().split())
    graph[start].append((end, weight))

def dijkstra(graph, start, num_nodes):
    dist = {node: float('inf') for node in range(1, num_nodes+1)}
    dist[start] = 0

    pq = [(0, start)]
    
    while pq:
        cur_d, u = heapq.heappop(pq)
        if cur_d > dist[u]:
            continue
        for v, weight in graph[u]:
            new_d = cur_d + weight
            if new_d < dist[v]:
                dist[v] = new_d
                heapq.heappush(pq, (new_d, v))

    return dist

shortest_paths = dijkstra(graph, k, v)

for node in range(1, v+1):
    distance = shortest_paths[node]
    print(distance if distance < float('inf') else "INF")
