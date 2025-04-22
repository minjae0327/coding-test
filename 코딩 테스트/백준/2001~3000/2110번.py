import sys

input = sys.stdin.readline

n, c = map(int, input().split())

houses = [int(input()) for _ in range(n)]
houses.sort()

result = 0
left = 1
right = houses[-1] - houses[0]

def get_interval(houses, mid, c):
    count = 1
    installed = houses[0]
    
    for i in range(1, n):
        if houses[i] - installed >= mid:
            count += 1
            installed = houses[i]
        if count >= c:
            return True

    return False

while left <= right:
    mid = (right + left) // 2
    
    interval = get_interval(houses, mid, c)
    
    if interval:
        result = mid
        left = mid + 1
    else:
        right = mid - 1

print(result)