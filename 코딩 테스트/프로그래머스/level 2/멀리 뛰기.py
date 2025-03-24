from collections import defaultdict

def solution(n):
    dict = defaultdict(int)
    dict[0] = 1
    dict[1] = 1
    
    if n == 1:
        return 1
    
    for i in range(2, n + 1):
        dict[i] = int((dict[i-2] + dict[i-1]) % 1234567)
        
        if i == n:
            return dict[i]
        
solution(4)