def solution(k, dungeons):
    answer = 0
    n = len(dungeons)
    
    def dfs(current_energy, count, visited):
        nonlocal answer
        # 최대 방문 횟수 갱신
        answer = max(answer, count)
        
        # 아직 방문하지 않은 던전 중 조건(최소 필요 에너지)을 만족하는 던전을 순회
        for i in range(n):
            if not visited[i] and current_energy >= dungeons[i][0]:
                visited[i] = True
                dfs(current_energy - dungeons[i][1], count + 1, visited)
                visited[i] = False  # 백트래킹
    
    dfs(k, 0, [False] * n)
    
    return answer


print(solution(80, [[80,20],[50,40],[30,10]]))