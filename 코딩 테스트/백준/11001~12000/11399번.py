#backjoon
N = int(input())

withdraws = []

withdraws = list(map(int, input().split(" ")))
    
withdraws = sorted(withdraws)

num = 0
result = 0
for i in range(N):
    num += + withdraws[i]
    result += num
    
print(result)