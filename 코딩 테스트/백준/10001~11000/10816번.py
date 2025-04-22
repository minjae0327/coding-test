import sys
from collections import defaultdict

input = sys.stdin.readline

dict_count = defaultdict(int)

n = int(input())
nums = list(map(int, input().split()))

for num in nums:
    dict_count[num] += 1

m = int(input())
finds = list(map(int, input().split()))

result = []
for find in finds:
    result.append(dict_count[find])

print(*result)