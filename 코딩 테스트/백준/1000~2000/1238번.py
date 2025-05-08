import sys
import heapq

input = sys.stdin.readline

N, M, destination = map(int, input().split())

graph = [[] for _ in range(N+1)]
reversed_graph = [[] for _ in range(N+1)]
for _ in range(M):
    start, end, weight = map(int, input().split())
    graph[start].append((end, weight))
    reversed_graph[end].append((start, weight))

def dijkstra(graph, start):
    dist = {node: float('inf') for node in range(1, N+1)}
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


dist1 = dijkstra(graph, destination)
dist2 = dijkstra(reversed_graph, destination)

max_cost = max(dist1[i] + dist2[i] for i in range(1, N+1))

print(max_cost)