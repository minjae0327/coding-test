n, d, k, c = map(int, input().split())
sushis = []

for _ in range(n):
    sushis.append(int(input()))

left = 0
right = k
result = 0

for i in range(n):
    if left > right:
        a = sushis[left:n]
        b = sushis[0:right+1]
        kinds = a + b
    else:
        kinds = sushis[left:right]
    kinds = set(kinds)
    
    if c not in kinds:
        kinds.add(c)
    if len(kinds) > result:
        result = len(kinds)
        
    left += 1
    if left > n:
        left = 0
        
    right += 1
    if right > n:
        right = 0
    
print(result)
