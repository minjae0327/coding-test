# backjoon
import sys

input = sys.stdin.readline
expressions = input().strip().split("-")

for i in range(len(expressions)):
    expression = expressions[i]
    if "+" in expression:
        nums = map(int, expression.split("+"))
        num = sum(nums)
        expressions[i] = num
    else:
        num = int(expression)
        expressions[i] = num

result = expressions[0]
for num in expressions[1:]:
    result -= num

print(result)