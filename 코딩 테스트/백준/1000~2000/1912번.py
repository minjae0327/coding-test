import sys
input = sys.stdin.readline

n = int(input())
arr = list(map(int, input().split()))

current = arr[0]
best = arr[0]

for x in arr[1:]:
    current = max(current + x, x)
    best = max(best, current)

print(best)
