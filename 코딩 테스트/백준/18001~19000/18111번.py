import sys

input = sys.stdin.readline

n, m, b = map(int, input().split())

terrain = [list(map(int, input().split())) for _ in range(n)]

min_height = min(map(min, terrain))
max_height = max(map(max, terrain))

best_time = float('inf')
best_height = 0

for height in range(min_height, max_height + 1):
    time = 0
    remove = 0
    add = 0
    
    for row in terrain:
        for block in row:
            if block > height:
                remove += block - height
            else:
                add += height - block
    
    if remove + b >= add:
        time = remove * 2 + add
        if time < best_time:
            best_time = time
            best_height = height
        if time == best_time:
            best_height = max(height, best_height)
            
print(best_time, best_height)