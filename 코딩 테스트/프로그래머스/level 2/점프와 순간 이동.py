def solution(n):
    cost = 0
    
    while n > 0:
        if n % 2 == 0:
            n = n // 2
        else:
            cost += 1
            n = n - 1
            
    return cost