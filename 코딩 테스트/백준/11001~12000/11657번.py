import sys

input = sys.stdin.readline

v, e = map(int, input().split())

edges = []

INF = float('inf')
dist = [INF] * (v + 1)

for _ in range(e):
    start, end, cost = map(int, input().split())
    edges.append((start, end, cost))
    
def bellmanford(start):
    dist[start] = 0
    
    for i in range(v):
        for j in range(e):
            cur_node, next_node, cost = edges[j]
            
            # 갈 수 있는 경로가 존재하고 현재까지 온 경로 비용 + 가야할 비용이 더 작다면
            if dist[cur_node] != INF and dist[cur_node] + cost < dist[next_node]:
                dist[next_node] = dist[cur_node] + cost
                
                # 갱신되지 않는다면 음의 사이클 존재
                if i == v-1:
                    return False
                
    return True

if bellmanford(1):
    for i in range(2, v+1):
        if dist[i] == INF:
            print(-1)
        else:
            print(dist[i])
else:
    print(-1)