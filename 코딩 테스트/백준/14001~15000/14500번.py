from collections import deque

def bfs(nums, x, y):
    visited = set()
    have_to_visit = deque()
    max_weight = 0
    
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    
    visited.add((x, y))
    have_to_visit.append((x, y, nums[x][y], 1, visited))
    
    while have_to_visit:
        x, y, weight, count, _visited = have_to_visit.popleft()
        
        if count == 4:
            if weight > max_weight:
                max_weight = weight
            continue
        
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            
            if 0 <= nx < n and 0 <= ny < m and (nx, ny) not in _visited:
                new_visited = set(_visited)
                new_visited.add((nx, ny))
                have_to_visit.append((nx, ny, weight + nums[nx][ny], count + 1, new_visited))
    
    return max_weight

def t_boundary(nums, x, y):
    max_weight = 0
        
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    for omit in range(4):
        total = nums[x][y]
        for d in range(4):
            if d == omit:
                continue
            nx = x + dx[d]
            ny = y + dy[d]

            if not (0 <= nx < n and 0 <= ny < m):
                break
            
            total += nums[nx][ny]
            
        if max_weight < total:
            max_weight = total
    
    return max_weight


n, m = map(int, input().split())
nums = [list(map(int, input().split())) for _ in range(n)]

max_weight = 0

for i in range(n):
    for j in range(m):
        a = bfs(nums, i, j)
        b = t_boundary(nums, i, j)
        
        max_weight = max(max_weight, a, b)
            
print(max_weight)