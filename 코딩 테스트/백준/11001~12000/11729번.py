n = int(input())

count = 0
movements = []

def hanoi(n, a, c, b):
    global count
    
    if n == 1:
        movements.append([a, c])
        count += 1
        return
    
    hanoi(n-1, a, b, c)
    movements.append([a, c])
    count += 1
    hanoi(n-1, b, c, a)
    

hanoi(n, 1, 3, 2)
print(count)
for row in movements:
    print(*row)