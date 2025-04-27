from collections import deque

a, b = map(int, input().split())

def bfs(start, end):
    have_to_visit = deque()
    INF = float("inf")
    visited = [INF] * 100001
    
    have_to_visit.append(start)
    visited[start] = 0

    while have_to_visit:
        start = have_to_visit.popleft()
        
        if start == end:
            return visited[end]
        
        for node, count in ((start * 2, 0), (start + 1, 1), (start - 1, 1)):
            if 0 <= node <= 100000 and visited[node] > visited[start] + count:
                visited[node] = visited[start] + count
                
                if count == 0:
                    have_to_visit.appendleft(node)
                else:
                    have_to_visit.append(node)
    

result = bfs(a, b)
print(result)
