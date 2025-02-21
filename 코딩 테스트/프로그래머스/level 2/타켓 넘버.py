def solution(numbers, target):
    sum_of_nums = sum(numbers)
    rest = (sum_of_nums-target) // 2
    length = len(numbers)
    
    def recursive(target, idx, cnt):
        for i in range(idx, length):
            temp = target
            temp -= numbers[i]
            
            if temp == 0:
                cnt += 1
            elif temp > 0:
                # 음수가 나오는 부분 다음부터 다시 탐색
                # 0이 될 때까지 순회
                cnt += recursive(temp, i+1, 0)
            elif temp < 0:
                continue
            
        return cnt
    
    return recursive(rest, 0, 0)
