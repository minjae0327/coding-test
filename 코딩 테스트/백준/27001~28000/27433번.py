n = int(input())

def factorial(n):
    if n == 1 or n == 0:
        return 1
    elif n == 2:
        return 2
    else:
        return factorial(n-1) * n

print(factorial(n))