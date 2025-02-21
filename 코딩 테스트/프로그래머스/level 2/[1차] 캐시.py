def solution(cacheSize, cities):
    cache = []

    running_time = 0
    
    if cacheSize == 0:
        return 5*len(cities)

    for i in range(cacheSize):
        city = cities[i].lower()
        
        if city in cache:
            cache.append(city)
            running_time += 1
        else:
            cache.append(city)
            running_time += 5
        
    for i in range(len(cache), len(cities)):
        city = cities[i].lower()
        
        if city in cache:
            cache.remove(city)
            cache.append(city)
            running_time += 1
            
        else:
            cache.pop(0)
            cache.append(city)
            running_time += 5
            
    return running_time