N, r, c = map(int, input().split(" "))
loc = 0

while N != 0:  
    N -= 1
    
    #4사분면    
    if r >= 2 ** N and c >= 2 ** N:
        r -= (2 ** N)
        c -= (2 ** N)
        loc += ((2 ** N) * (2 ** N)) * 3
    #3사분면
    elif r >= 2 ** N and c < 2 ** N:
        r-= (2 ** N)
        loc += ((2 ** N) * (2 ** N)) * 2
    #2사분면
    elif r < 2 ** N and c < 2 ** N:
        pass
    #1사분면
    else:
        c -= (2 ** N)
        loc += ((2 ** N) * (2 ** N))
        
print(loc)