import sys
sys.setrecursionlimit(10**6)

n, m = map(int, input().split()) 

cases = [list(map(int, input().split())) for _ in range(m)]

parent = [i for i in range(n+1)]

def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x]) #경로 압축
        
    return parent[x]

def union(parent, a_root, b_root):
    if a_root < b_root:
        parent[b_root] = a_root
    else:
        parent[a_root] = b_root
        

for i in range(m):
    case, a, b = cases[i]
    a_root = find(parent, a)
    b_root = find(parent, b)
    
    if case == 0:
        if a_root != b_root:
            union(parent, a_root, b_root)
    elif case == 1:
        if a_root != b_root:
            print("NO")
        else:
            print("YES")