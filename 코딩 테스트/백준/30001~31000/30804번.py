import sys
from collections import defaultdict

input = sys.stdin.readline

n = int(input())
num = list(map(int, input().split()))

count_dict = defaultdict(int)
a, b = 0, 0
result = 0

while b < n:
    count_dict[num[b]] += 1
    
    while len(count_dict) > 2:
        count_dict[num[a]] -= 1
        if count_dict[num[a]] == 0:
            del count_dict[num[a]]
        a += 1
    
    result = max(result, b - a + 1)
    b += 1

print(result)
