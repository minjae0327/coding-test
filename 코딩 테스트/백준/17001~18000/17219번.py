# backjoon
import sys
from collections import defaultdict

input = sys.stdin.readline

n, m = map(int, input().split())

dict1  = defaultdict(str)

for i in range(n):
    site, pw = input().split()
    dict1[site] = pw

for _ in range(m):
    site = input().strip()
    print(dict1[site])