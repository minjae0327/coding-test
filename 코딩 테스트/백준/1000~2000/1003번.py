#backjoon
def fibo(num):
    one, zero = 0, 0
    if num == 0:
        return zero + 1, one
    elif num == 1:
        return zero, one + 1
    else:
        fib = 1
        now = [0, 1]
        prev = [1, 0]
        while fib < num:
            fib += 1
            _next = [now[0] + prev[0], now[1] + prev[1]]
            prev = now
            now = _next
            
        return now[0], now[1]

T = int(input())

tast_case = []

for _ in range(T):
    tast_case.append(int(input()))
    
for i in range(T):
    a = fibo(tast_case[i])[0]
    b = fibo(tast_case[i])[1]
    print(a, b)