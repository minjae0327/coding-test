def solution(clothes):
    answer = 1
    _answer = 0
    
    dict = {}

    for cloth in clothes:
        if cloth[1] not in dict:
            dict[cloth[1]] = []
            
        dict[cloth[1]].append(cloth[0])
    
    for i in dict:
        _answer = len(dict[i]) + 1
        answer *= _answer
    
    return answer - 1