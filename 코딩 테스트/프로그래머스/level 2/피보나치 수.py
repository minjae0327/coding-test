def get_fib_num(n):
    a = 0
    b = 1
    
    for i in range(n):
        a, b = b, a+b
        
    return a

def solution(n):
    div = 1234567
    fib = get_fib_num(n)
    
    return fib % div