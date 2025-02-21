def solution(n,a,b):
    partipants = [i+1 for i in range(n)]
    list = []
    
    count = 1
    
    while True:
        for i in range(0, len(partipants), 2):
            n1 = partipants[i]
            n2 = partipants[i+1]
            c = [n1, n2]
            
            if a in c and b in c:
                return count
            
            if a in c:
                list.append(a)
            elif b in c:
                list.append(b)
            else:
                list.append(n1)
    
        count += 1
        partipants = list
        list = []
        
    return count