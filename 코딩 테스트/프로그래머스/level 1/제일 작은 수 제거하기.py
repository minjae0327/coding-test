def solution(arr):
    answer = []
    
    if len(arr) == 1:
       answer.append(-1)
       return answer
   
    min_num = arr[0]
    min_loc = 0
    
    for i in range(1, len(arr)):
        if arr[i] < min_num:
            min_num = arr[i]
            min_loc = i
            
    arr.pop(min_loc)
    answer = arr  
    
    return answer