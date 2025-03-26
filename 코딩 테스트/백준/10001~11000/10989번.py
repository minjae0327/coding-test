import sys

N = int(sys.stdin.readline())

count_dict = {i: 0 for i in range(1, 10001)}

for _ in range(N):
    num = int(sys.stdin.readline())
    count_dict[num] += 1

for key in range(1, 10001):
    if count_dict[key] != 0:
        for _ in range(count_dict[key]):
            print(key)
