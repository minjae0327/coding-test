import sys

input = sys.stdin.readline

n = int(input())

distances = list(map(int, input().split()))
prices = list(map(int, input().split()))

low_price = float("inf")

result = 0

for i in range(n-1):
    price = prices[i]
    
    if price < low_price:
        low_price = price
        
    result += low_price * distances[i]
        
print(result)