import sys

input = sys.stdin.readline

n,k = map(int, input().split())

coins = []

for _ in range(n):
    coins.append(int(input()))
    
coins = sorted(coins, reverse=True)

result = 0

for i in range(n):
    coin = coins[i]
    
    if k >= coin:
        result += k // coin
        k = k % coin
        
print(result)