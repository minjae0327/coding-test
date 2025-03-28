# backjoon
import sys
from collections import Counter

N = int(sys.stdin.readline())
nums = [int(sys.stdin.readline()) for _ in range(N)]

# 1. 산술평균
mean = int(round(sum(nums) / N))
sys.stdout.write(str(mean) + '\n')

# 2. 중앙값
nums.sort()
median = nums[N // 2]
sys.stdout.write(str(median) + '\n')

# 3. 최빈값
counter = Counter(nums)
max_count = max(counter.values())
modes = [k for k, v in counter.items() if v == max_count]
if len(modes) > 1:
    sys.stdout.write(str(sorted(modes)[1]) + '\n')
else:
    sys.stdout.write(str(modes[0]) + '\n')

# 4. 범위
sys.stdout.write(str(nums[-1] - nums[0]) + '\n')
