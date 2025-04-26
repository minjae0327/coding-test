import sys
import heapq

input = sys.stdin.readline

v, e = map(int, input().split())

graph = [[] for _ in range(v+1)]
for _ in range(e):
    start, end, weight = map(int, input().split())
    graph[start].append((end, weight))
    graph[end].append((start, weight))# 무향 그래프
    
must_visit1, must_visit2 = map(int, input().split())

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

shortest_paths1 = dijkstra(graph, 1, v)
shortest_paths2 = dijkstra(graph, must_visit1, v)
shortest_paths3 = dijkstra(graph, must_visit2, v)

# 1 → must_visit1 → must_visit2 → v
path1 = shortest_paths1[must_visit1] + shortest_paths2[must_visit2] + shortest_paths3[v]
# 1 → must_visit2 → must_visit1 → v
path2 = shortest_paths1[must_visit2] + shortest_paths3[must_visit1] + shortest_paths2[v]

answer = min(path1, path2)
print(answer if answer < float('inf') else -1)