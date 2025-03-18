def solution(s):
    while True:
        length = len(s)
        if length == 0:
            return 1
        
        for i in range(length-1):
            if s[i] == s[i+1]:
                s.remove(s[i])
                s.remove(s[i])
                break
            
        if length == len(s):
            return 0
        
solution("baabaa")