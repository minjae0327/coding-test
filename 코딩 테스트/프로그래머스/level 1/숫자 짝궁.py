from collections import Counter
    
def solution(x, y):
    answer = []
    
    counter = Counter(y)
    
    for num in x:
        if counter[num] > 0:
            counter[num] -= 1
            answer.append(num)
    
    answer.sort(reverse=True)   
    if len(answer) == 0:
        return "-1"
    elif len(answer) == answer.count("0"):
        return "0"
    return "".join(answer)