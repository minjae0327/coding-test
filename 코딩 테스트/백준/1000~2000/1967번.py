from collections import defaultdict, deque

n = int(input())

tree = defaultdict(list)

for _ in range(n-1):
    start, end, weight = map(int, input().split())
    tree[start].append((end, weight))
    tree[end].append((start, weight))
            
def dfs(tree, start):
    _tree = {i:0 for i in range(1, n+1)}
    visited = set()
    have_to_visit = deque()
    
    have_to_visit.append((start, 0))
    visited.add(start)
    
    while have_to_visit:
        node, weight = have_to_visit.popleft()
        _tree[node] = weight
        
        for next_node, next_weight in tree[node]:
            if next_node not in visited:
                have_to_visit.appendleft((next_node, weight + next_weight))
                visited.add(next_node)

    return _tree
    
    
_tree = dfs(tree, 1)
_node = max(_tree, key=_tree.get)
_tree = dfs(tree, _node)
print(max(_tree.values()))