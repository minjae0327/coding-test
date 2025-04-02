# backjoon
import sys
sys.setrecursionlimit(10**6)
input = sys.stdin.readline
from collections import defaultdict

def count_connection(edges, n):
    graph = defaultdict(list)

    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    count = 0

    def dfs(v):
        visited.add(v)
        for neighbor in graph[v]:
            if neighbor not in visited:
                dfs(neighbor)

    for node in range(1, n + 1):
        if node not in visited:
            dfs(node)
            count += 1

    return count

N, M = map(int, input().strip().split())
edges = [tuple(map(int, input().strip().split())) for _ in range(M)]
    
print(count_connection(edges, N)) 