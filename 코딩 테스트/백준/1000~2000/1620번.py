# backjoon
import sys
from collections import defaultdict

input = sys.stdin.readline

n, m = map(int, input().split())

dict1  = defaultdict(str)
dict2 = defaultdict(int)

for i in range(1, n+1):
    pokemon = input().strip()
    dict1[i] = pokemon
    dict2[pokemon] = i

for _ in range(m):
    query = input().strip()
    if query.isdigit():
        print(dict1[int(query)])
    else:
        print(dict2[query])