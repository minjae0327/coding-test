N = int(input())
prime_candidates = list(map(int, input().split(" ")))
result = 0

for n in prime_candidates:
    if n < 2:
        continue
        
    is_prime = True
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            is_prime = False
            break
        
    if is_prime:
        result += 1
        
print(result)
