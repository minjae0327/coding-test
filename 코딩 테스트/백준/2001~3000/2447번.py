n = int(input())

grid = [["*" for _ in range(n)] for _ in range(n)]

def recursive(x, y, n):
    if n == 1:
        return
    
    n = n // 3
    
    for i in range(x + n, x + n * 2):
        for j in range(y + n, y + n * 2):
            grid[i][j] = " "
            
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                    continue
            
            recursive(x + i * n, y + j * n, n)

recursive(0, 0, n)

for row in grid:
    print("".join(row))
