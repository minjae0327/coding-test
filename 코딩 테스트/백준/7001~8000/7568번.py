n = int(input())

mans = [list(map(int, input().split())) for _ in range(n)]

def is_smaller(a, b):
    return a[0] < b[0] and a[1] < b[1]

length = len(mans)
scores = []

for man in mans:
    score = 1
    for i in range(length):
        if mans[i] == man:
            continue
        
        std = is_smaller(man, mans[i])
        if std:
            score += 1
            
    scores.append(score)
    
print(*scores)