def solution(friends, gifts):
    gift_size = len(friends)
    
    trade = [[0 for i in range(gift_size)] for j in range(gift_size)]
    
    friend_dict = {}
    for i in range(len(friends)):
        friend_dict[friends[i]] = i
        
    for i in range(len(gifts)):
        _from, _to = gifts[i].split(" ")
        
        trade[friend_dict[_from]][friend_dict[_to]] += 1
        
    trade_index = [[0 for i in range(3)] for j in range(gift_size)]
    
    for i in range(len(trade)):
        send_gifts = sum(trade[i])
        receive_gifts=0
        for j in range(len(trade)):
            receive_gifts += trade[j][i]
        
        trade_index[i][0] = send_gifts
        trade_index[i][1] = receive_gifts
        trade_index[i][2] = send_gifts - receive_gifts
        
    answer = 0
    
    #두 사람 사이에 더 많은 선물을 준 사람이 다음 달에 선물을 하나 받습니다.
    # 두 사람이 선물을 주고받은 기록이 하나도 없거나 주고받은 수가 같다면, 
    # 선물 지수가 더 큰 사람이 선물 지수가 더 작은 사람에게 선물을 하나 받습니다.
    # 선물 지수 = 준 선물 - 받은 선물
    # 선물 지수도 같다면 다음달에는 선물을 주고받지 않습니다.
    need_to_get = friend_dict.copy()

    for key in need_to_get:
        need_to_get[key] = 0
    
    for i in range(len(friends)):
        target = friends[i]

        for j in range(i, len(friends)):
            if i == j:
                continue
            
            friend = friends[j]
            
            target_to_friend = trade[i][j]
            friend_to_target = trade[j][i]
            
            if target_to_friend > friend_to_target:
                need_to_get[target] += 1
            elif target_to_friend < friend_to_target:
                need_to_get[friend] += 1
            elif (target_to_friend == friend_to_target) or (target_to_friend == 0 and friend_to_target == 0):
                target_index = trade_index[friend_dict[target]][2]
                friend_index = trade_index[friend_dict[friend]][2]
                
                if target_index > friend_index:
                    need_to_get[target] += 1
                elif target_index < friend_index:
                    need_to_get[friend] += 1
    
    max_key = 0

    for friend in friends:
        if need_to_get[friend] > max_key:
            max_key = need_to_get[friend]
    
    return max_key