def solution(toppings):
    count = 0
    length = len(toppings)
    
    left_topping = [0] * length
    right_topping = [0] * length
    left_unique = set()
    right_unique = set()
    
    for i in range(length):
        left_unique.add(toppings[i])
        left_topping[i] = len(left_unique)
    for i in range(length-1, -1, -1):
        right_unique.add(toppings[i])
        right_topping[i] = len(right_unique)
        
    for i in range(length-1):
        if left_topping[i] == right_topping[i+1]:
            count += 1
        
            
    return count