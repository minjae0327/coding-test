# backjoon
import sys
from itertools import permutations

input = sys.stdin.readline

n, m = map(int, input().split())

nums = list(map(int, input().split()))
perm = list(permutations(nums, m))
perm = list(set(perm))
perm = sorted(perm)
for i in range(len(perm)):
    print(" ".join(map(str, perm[i])))