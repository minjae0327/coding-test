def solution(id):
    
    id = id.lower()
    id = ''.join(filter(lambda char: char == '_' or char == '-' or char == '.' or 'a' <= char <= 'z' or '0' <= char <= '9', id))
    answer = ""
    for i in range(len(id)):
        if id[i] == '.' and i + 1 < len(id) and id[i+1] == '.':
            continue
            
        answer += id[i]
        
    if answer[0] == '.':
        answer = answer[1:]
        if len(answer) == 0:
            answer = "a"
    if answer[-1] == '.':
        answer = answer[:-1]
        if len(answer) == 0:
            answer = "a"
    

    if len(answer) >= 16:
        answer = answer[:15]
        if answer[-1] == '.':
            answer = answer[:14]
            
    if len(answer) <= 2:
        alp = answer[-1]
        while(len(answer) < 3):
            answer += alp
            
    return answer