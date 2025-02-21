def check_correction(str):
    stack = []
    
    for i in range(len(str)):
        stack.append(str[i])
        
        if (str[0] == ")" or str[-1] == "(") or\
            (str[0] == "}" or str[-1] == "{") or\
            (str[0] == "]" or str[-1] == "["):
            answer = False
            return answer
        
        if len(stack) > 1:    
            if stack[-1] == ")" and stack[-2] == "(":
                stack.pop()
                stack.pop()
            elif stack[-1] == "]" and stack[-2] == "[":
                stack.pop()
                stack.pop()
            elif stack[-1] == "}" and stack[-2] == "{":
                stack.pop()
                stack.pop()
                
    if len(stack) == 0:
        return True
    else:
        return False

def solution(s):
    answer = 0
    
    for _ in range(len(s)):
        last_s = list(s).pop(0)
        s = s[1:] + last_s  
        
        if check_correction(s):
            answer += 1
    
    return answer
    