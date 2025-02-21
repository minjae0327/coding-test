lotto = {6 : 1,
         5 : 2,
         4 : 3,
         3 : 4,
         2 : 5,
         1 : 6,
         0 : 6}

def solution(lottos, win_nums):
    low_lotto = 0
    for i in range(len(lottos)):
        for j in range(len(win_nums)):
            if lottos[i] == win_nums[j]:
                low_lotto += 1
                win_nums.pop(j)
                break
            
    high_lotto = low_lotto
    high_lotto += sum(map(lambda x : x == 0, lottos))
            
    return [lotto[high_lotto], lotto[low_lotto]]