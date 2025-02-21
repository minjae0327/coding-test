def solution(bandage, maxHP, monsterStat):
    def get_health(time, t, x, y, maxHP, currentHP):
        while(time > 0):
            if time - t >= 0:
                currentHP += t*x+y
                time -= t
            else:
                currentHP += time * x
                time -= time
        
        return min(currentHP, maxHP)

    t = bandage[0]
    x = bandage[1]
    y = bandage[2]

    prev_time = 0
    currentHP = maxHP

    for monster in monsterStat:
        time = monster[0]
        att = monster[1]
        
        if time - prev_time > 1:
            currentHP = get_health(time - (prev_time + 1), t, x, y, maxHP, currentHP)
        
        currentHP -= att
        if currentHP <= 0:
            return -1
        
        prev_time = time
        
    return currentHP


print(solution([1, 1, 1], 5, [[1, 2], [3, 2]]))