# backjoon
import sys
from itertools import combinations

input = sys.stdin.readline

n, m = map(int, input().split())

nums = [i for i in range(1, n+1)]

perm = list(combinations(nums, m))
for i in range(len(perm)):
    print(" ".join(map(str, perm[i])))

