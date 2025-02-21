def solution(s):
    answer = True
    
    stack = []
    
    for i in range(len(s)):
        if s[0] == ")" or s[-1] == "(":
            answer = False
            return answer
        
        stack.append(s[i])
        
        if len(stack) > 1:
            if stack[-1] == ")" and stack[-2] == "(":
                stack.pop()
                stack.pop()
                
    if len(stack) == 0:
        return True
    else:
        return False
    