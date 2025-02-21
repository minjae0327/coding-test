def solution(id_list, reports, k):
    reported = {}
    ban_list = []
    result = []

    for id in id_list:
        reported[id] = {"count":0, "reported_ids" : [], "banned" : []}

    for report in reports:
        report_id, reported_id = report.split(' ')
        
        if reported_id not in reported[report_id]['reported_ids']:
            reported[report_id]['reported_ids'].append(reported_id)
            reported[reported_id]['count'] += 1
    
    for user in reported:
        if reported[user]['count'] >= k:
            ban_list.append(user)

    for user in reported:
        num = 0
        
        for ban in ban_list:
            if ban in reported[user]['reported_ids']:
                num += 1
                
        result.append(num)
        
    
    return result

print(solution(["muzi", "frodo", "apeach", "neo"], 
               ["muzi frodo","apeach frodo","frodo neo","muzi neo","apeach muzi"], 2))
print(solution(["con", "ryan"], ["ryan con", "ryan con", "ryan con", "ryan con"], 3))
print(solution(["abc", "acd", "add", "abd"], 
               ["abc abd", "abc add", "acd abd", "abc abd", "add abd"], 2))