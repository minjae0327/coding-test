from itertools import combinations

n = int(input())
status = [list(map(int, input().split())) for _ in range(n)]

players = list(range(n))  # [0, 1, 2, 3]

combi = list(combinations(players, n // 2))  # [(0,1), (0,2), ..., (2,3)]

result = float("inf")
length = len(combi) // 2

for i in range(length):
    team1 = combi[i]
    team2 = combi[-(i + 1)]
    
    def get_score(team):
        score = 0
        for a, b in combinations(team, 2):
            score += status[a][b] + status[b][a]
        return score
    
    min_score = abs(get_score(team1) - get_score(team2))
    
    result = min(result, min_score)
    
    
print(result)