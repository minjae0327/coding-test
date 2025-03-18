def solution(s):
    s = s.lower()

    s_list = s.split(" ")

    for i in range(len(s_list)):
        if s_list[i] and ("a" <= s_list[i][0] <= "z"):
            s_list[i] = s_list[i][0].upper() + s_list[i][1:]
            
            
    answer = " ".join(s_list)
    
    return answer