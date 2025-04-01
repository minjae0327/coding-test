# backjoon
N, M = map(int, input().split(" "))

nums = list(map(int, input().split(" ")))
prefix_num = [0] * N
prefix_num[0] = nums[0]
for i in range(1, N):
    prefix_num[i] = prefix_num[i-1] + nums[i]

ranges = []
for _ in range(M):
    ranges.append(list(map(int, input().split(" "))))
    
for _range in ranges:
    i = _range[0] - 1
    j = _range[1]
    
    if i == 0:
        print(prefix_num[j - 1])
    else:
        print(prefix_num[j - 1] - prefix_num[i - 1])
