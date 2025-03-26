a, b = map(int, input().split(" "))

for n in range(a, b+1):
    if n < 2:
        continue
        
    is_prime = True
    result = 0
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            is_prime = False
            break
        
    if is_prime:
        print(n)
