n = int(input())

result = 0

for j in range(1, n):
    digit_sum = sum(int(d) for d in str(j))
    if j + digit_sum == n:
        result = j
        break

print(result)
