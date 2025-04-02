# backjoon
import sys
input = sys.stdin.readline

N, M = map(int, input().strip().split())
trees = list(map(int, input().strip().split()))

left = 1
right = max(trees)
result = 0

while left <= right:
    mid = (left + right) // 2
    total = sum(tree - mid for tree in trees if tree > mid)
            
    if total >= M:
        result = mid
        left = mid + 1
    else:
        right = mid - 1
    
print(result)