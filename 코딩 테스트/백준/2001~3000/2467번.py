n = int(input())
liquids = list(map(int, input().split()))
liquids = sorted(liquids)

L = 0
R = n-1

result1 = 0
result2 = 0

comp = float("inf")

while L < R:
    answer = liquids[L] + liquids[R]
    
    if comp > abs(answer):
        comp = abs(answer)
        result1 = L
        result2 = R
        
    if answer > 0:
        R -= 1
    elif answer < 0:
        L += 1
    else:
        break
    
print(liquids[result1], liquids[result2])