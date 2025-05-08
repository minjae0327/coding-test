import sys

input = sys.stdin.readline

def check_negative_cycle(n, edges):
    dist = [0] * (n+1)
    
    for i in range(n):
        updated = False
        for start, end, weight in edges:
            if dist[start] + weight < dist[end]:
                dist[end] = dist[start] + weight
                updated = True
                if i == n-1:
                    return True
        if not updated:
            break
    
    return False

tc = int(input())

for i in range(tc):
    N, M, W = map(int, input().split())

    edges = []

    for _ in range(M):
        start, end, cost = map(int, input().split())
        edges.append((start, end, cost))
        edges.append((end, start, cost))
    for _ in range(W):
        start, end, cost = map(int, input().split())
        cost *= -1
        edges.append((start, end, cost))


    if check_negative_cycle(N, edges):
        print("YES")  # 음의 사이클 없음
    else:
        print("NO")  # 음의 사이클 존재
