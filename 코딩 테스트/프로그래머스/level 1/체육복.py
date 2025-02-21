def solution(n, lost, reserve):
    lost = sorted(lost)

    students = {}

    for i in range(n+2):
        students[i] = 0
        
    for have in reserve:
        students[have] = 2
        
    for _lost in lost:
        if students[_lost] == 2:
            students[_lost] = 1
        else:
            students[_lost] = -1
        
    for i in range(n):
        if students[i+1] == 0:
            students[i+1] = 1
        
    for _lost in lost:
        if students[_lost-1] == 2:
            students[_lost-1] = 1
            students[_lost] = 1
            
        elif students[_lost+1] == 2:
            students[_lost+1] = 1
            students[_lost] = 1
    
    answer = 0
    
    for i in range(1, n+1):
        if students[i] >= 1:
            answer += 1
    
    return answer