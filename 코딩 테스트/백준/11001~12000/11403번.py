def floyd_warshall(matrix, n):
    reach = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if matrix[i][j]:
                reach[i][j] = 1
                
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if reach[i][k] == reach[k][j]:
                    reach[i][j] = 1
    
    return reach

n = int(input())
matrix = [list(map(int, input().split())) for _ in range(n)]

result = floyd_warshall(matrix, n)
for row in result:
    print(*row)