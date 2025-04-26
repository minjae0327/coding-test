from collections import deque

a, b = map(int, input().split())

def bfs(start, end):
    have_to_visit = deque()
    count = 0
    
    have_to_visit.append((start, count))
    
    while have_to_visit:
        node, count = have_to_visit.popleft()
        
        if node == end:
            return count
        elif node > end:
            continue
        
        have_to_visit.append((int(str(node) + '1'), count + 1))
        have_to_visit.append((node * 2, count + 1))
        
    return -1

result = bfs(a, b)

if result == -1:
    print(-1)
else:
    print(result + 1)