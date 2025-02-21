def solution(players, callings):
    dict = {}
    for i in range(len(players)):
        dict[players[i]] = i
        
    for call in callings:
        loc = dict[call]
        
        temp = players[loc]
        players[loc] = players[loc-1]
        players[loc-1] = temp
        
        temp = dict[call] #kai
        dict[call] = dict[players[loc]]
        dict[players[loc]] = temp
        
    return players