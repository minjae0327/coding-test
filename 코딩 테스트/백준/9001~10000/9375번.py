# backjoon
import sys
from collections import defaultdict

input = sys.stdin.readline

n = int(input())

for _ in range(n):
    result = 1
    t = int(input())
    dict1 = defaultdict(list)

    for _ in range(t):
        cloth, kind = input().split()
        dict1[kind].append(cloth)
        
    for kind in dict1:
        result *= len(dict1[kind]) + 1
        
    print(result-1)