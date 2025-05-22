a, b, c, d, e, f = map(int, input().split())

def solve(a, b, c, d, e, f):
    for x in range(-999, 1000):
        for y in range(-999, 1000):
            if a*x + b*y == c and d*x + e*y == f:
                print(x, y)
                return
                
solve(a, b, c, d, e, f)
