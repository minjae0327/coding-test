# backjoon
import sys

input = sys.stdin.readline

N = int(input())
coords = list(map(int, input().strip().split()))

coordinates = sorted(set(coords))
coordinates

coord_dict = {}

for i in range(len(coordinates)):
    coord_dict[coordinates[i]] = i

coord_dict

result = [coord_dict[i] for i in coords]
print(*result, sep=(" "))