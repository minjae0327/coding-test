from collections import defaultdict, deque

n = int(input())
tree = defaultdict(list)

for _ in range(n):
    data = list(map(int, input().split()))
    node = data[0]
    i = 1
    
    while data[i] != -1:
        nei = data[i]
        w   = data[i+1]
        tree[node].append((nei, w))
        tree[nei].append((node, w))
        i += 2

def dfs(tree, start):
    _tree = {i: 0 for i in range(1, n+1)}
    visited = set()
    have_to_visit = deque()

    have_to_visit.append((start, 0))
    visited.add(start)

    while have_to_visit:
        node, weight = have_to_visit.popleft()
        _tree[node] += weight
        
        for _node, _weight in tree[node]:
            if _node not in visited:
                have_to_visit.appendleft((_node, weight + _weight))
                visited.add(_node)
                
    return _tree
        

_tree = dfs(tree, 1)
_node = max(_tree, key=_tree.get)
_tree = dfs(tree, _node)
print(max(_tree.values()))