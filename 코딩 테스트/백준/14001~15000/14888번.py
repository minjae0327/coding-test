from itertools import combinations, permutations

n = int(input())
nums = list(map(int, input().split()))
count = list(map(int, input().split()))
operators = ["+", "-", "*", "/"]

ops = []
for i in range(4):
    ops += [operators[i]] * count[i]

a = set(permutations(ops, n-1))

min_value = float("inf")
max_value = -float("inf")

for op_seq in a:
    total = nums[0]
    for op, x in zip(op_seq, nums[1:]):
        if op == "+":
            total = total + x
        elif op == "-":
            total = total - x
        elif op == "*":
            total = total * x
        else:
            total = int(total / x)

    min_value = min(min_value, total)
    max_value = max(max_value, total)

print(max_value)
print(min_value)
