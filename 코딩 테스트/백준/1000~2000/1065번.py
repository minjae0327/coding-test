n = int(input())

result = 0
if n < 100:
    result = n
else:
    result = 99
    for i in range(100, n + 1):
        i = str(i)
        
        num1 = int(i[0])
        num2 = int(i[1])
        num3 = int(i[2])
        
        diff1 = num1 - num2
        diff2 = num2 - num3
        
        if diff1 == diff2:
            result += 1

print(result)