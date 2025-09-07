from collections import Counter

n, c = map(int, input().split())

nums = list(map(int, input().split()))

count = Counter(nums)
count = count.most_common()
count.sort(key=lambda x: -x[1])

result = []

for data in count:
    num, iteration = data
    for _ in range(iteration):
        result.append(num)
        
print(*result)