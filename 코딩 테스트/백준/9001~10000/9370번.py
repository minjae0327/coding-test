import sys
import heapq

INF = float("inf")
input = sys.stdin.readline

def dijkstra(maps, start, num_nodes):
    dist = {node : INF for node in range(1, num_nodes + 1)}
    dist[start] = 0
    
    queue = [(0, start)]
    
    while queue:
        current_dist, start = heapq.heappop(queue)
        
        if current_dist > dist[start]:
            continue
        
        for end, weight in maps[start]:
            new_dist = weight + current_dist
            
            if dist[end] > new_dist:
                dist[end] = new_dist
                heapq.heappush(queue, (new_dist, end))
                
    return dist

T = int(input())

for _ in range(T):
    n, m, t = map(int, input().split())
    s, g, h = map(int, input().split())
    
    maps = [[] for _ in range(n+1)]

    for _ in range(m):
        start, end, weight = map(int, input().split())
        maps[start].append((end, weight))
        maps[end].append((start, weight))

    shortest_path1 = dijkstra(maps, s, n)
    shortest_path2 = dijkstra(maps, g, n)
    shortest_path3 = dijkstra(maps, h, n)
    
    destinations = []
    
    for i in range(t):
        destination = int(input())
        
        path1 = shortest_path1[g] + shortest_path2[h] + shortest_path3[destination]
        path2 = shortest_path1[h] + shortest_path3[g] + shortest_path2[destination]
        
        path = min(path1, path2)
        
        if path != INF and shortest_path1[destination] == path:
            destinations.append(destination)
        
    result = sorted(destinations)
    print(*result)
