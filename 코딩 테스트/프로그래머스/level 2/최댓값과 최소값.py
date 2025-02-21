def solution(s):
    alp_list = s.split(" ")
    
    alp_list = list(map(int, alp_list))
    
    min_num = str(min(alp_list))
    max_num = str(max(alp_list))
    
    answer = str(min_num + " " + max_num)
    
    return answer
    
    