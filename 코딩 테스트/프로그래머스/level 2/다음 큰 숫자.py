def solution(n):
    bin_n = bin(n)[2:]
    bin_n = bin_n.replace("0", "")
    len_n = len(bin_n)

    while True:
        n += 1
        
        bin_n = bin(n)[2:]
        bin_n = bin_n.replace("0", "")
        _len_n = len(bin_n)
        
        if len_n == _len_n:
            return n