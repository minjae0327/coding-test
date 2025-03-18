def solution(s):
    c = 0
    count = 0
    length = 0

    while c != 1:
        len_s = len(s)
        s = s.replace("0", "")
        len_zero = len(s)
        length += len_s - len_zero
        
        c = len(s)
        s = bin(c)[2:]
        
        count += 1
        
        if c == 1:
            return [count, length]