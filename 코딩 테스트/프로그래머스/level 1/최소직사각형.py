def solution(sizes):
    answer = 0
    
    list = []
    
    max1, max2 = 0, 0
    
    for i in range(len(sizes)):
        list.append(sorted(sizes[i]))
        if list[i][0] > max1:
            max1 = list[i][0]
        if list[i][1] > max2:
            max2 = list[i][1]
            
            
    answer = max1 * max2
    
    return answer