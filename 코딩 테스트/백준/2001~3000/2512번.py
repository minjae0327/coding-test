import sys

input = sys.stdin.readline

n = int(input())
requests = list(map(int, input().split()))
budget = int(input())

city_budget = 0

start = 0
end = max(requests)

if sum(requests) < budget:
    city_budget = end
else:
    while start <= end:
        mid = (start + end) // 2
        
        total = 0
        for i in range(n):
            total += min(mid, requests[i])
        
        if budget >= total:
            city_budget = mid
            start = mid + 1
        else:
            end = mid - 1
            
print(city_budget)