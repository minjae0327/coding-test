import sys
sys.setrecursionlimit(10**6)

def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x]) #경로 압축
        
    return parent[x]

def union(parent, a_root, b_root):
    if a_root < b_root:
        parent[b_root] = a_root
    else:
        parent[a_root] = b_root
    
def kruskal(edges, n):
    edges.sort(key = lambda x : x[2])
    parent = [i for i in range(n + 1)]
    
    mst_weight = 0
    # mst_edges = []
    
    for a, b, weight in edges:
        a_root = find(parent, a)
        b_root = find(parent, b)
        if a_root != b_root:
            union(parent, a_root, b_root)
            mst_weight += weight
            # mst_edges.append((a, b, weight))
            
    return mst_weight


v, e = map(int, input().split())

edges = []

for i in range(e):
    start, end, weight = map(int, input().split())
    edges.append((start, end, weight))

weight = kruskal(edges, v)
print(weight)