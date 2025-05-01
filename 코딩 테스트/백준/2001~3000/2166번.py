n = int(input())

coords = [list(map(int, input().split())) for _ in range(n)]
coords.append([coords[0][0], coords[0][1]])

result1 = 0
result2 = 0

for i in range(n):
    if i == n-1:
        a = i
        b = 0
    else:
        a = i
        b = i+1
        
    result1 += coords[a][0] * coords[b][1]
    result2 += coords[b][0] * coords[a][1]
    
print(abs(result1 - result2) / 2)