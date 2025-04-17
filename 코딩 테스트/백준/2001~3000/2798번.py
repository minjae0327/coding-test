import sys
from itertools import combinations

input = sys.stdin.readline

n, m = map(int, input().split())
cards = list(map(int, input().split()))

nums = []

a = list(combinations(cards, 3))
for i in range(len(a)):
    nums.append(sum(a[i]))

candidates = [x for x in nums if x <= m]

closest = max(candidates)
print(closest)