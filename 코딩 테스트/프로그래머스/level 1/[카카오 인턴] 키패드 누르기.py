def check_position(l_pos, r_pos, num, hand):
    l_weight = abs(l_pos - num)
    l_weight = (l_weight // 3) + (l_weight % 3)
    
    r_weight = abs(r_pos - num)
    r_weight = (r_weight // 3) + (r_weight % 3)
    
    if l_weight == r_weight:
        return hand
    elif l_weight < r_weight:
        return "L"
    else:
        return "R"

def solution(numbers, hand):
    hand = "R" if hand == "right" else "L"

    answer = ''

    left_num = [1, 4, 7]
    right_num = [3, 6, 9]

    pos = {
        "L" : 10,
        "R" : 12
    }

    for num in numbers:
        if num == 0:
            num = 11
            
        if num in left_num:
            answer = answer + "L"
            pos["L"] = num
        elif num in right_num:
            answer = answer + "R"
            pos["R"] = num
        else:
            _hand = check_position(pos["L"], pos["R"], num, hand)
            answer = answer + _hand
            pos[_hand] = num
            
    return answer