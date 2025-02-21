def solution(s):
    answer = True
    
    for i in range(len(s)):
        if not (len(s) == 4 or len(s) == 6):
            return False
        
        if 48 <= ord(s[i]) <= 57:
            int(s[i])
            continue
        else:
            answer = False
            break
    
    return answer