from collections import Counter

def multiset_intersection(list1, list2):
    counter1 = Counter(list1)
    counter2 = Counter(list2)
    
    intersection = list((counter1 & counter2).elements())
    
    return intersection

def multiset_sum(list1, list2):
    counter1 = Counter(list1)
    counter2 = Counter(list2)
    
    _sum = list((counter1 | counter2).elements())
    
    return _sum

def solution(str1, str2):
    A = []
    B = []

    for i in range(len(str1)-1):
        if (("a" <= str1[i] <= "z" or "A" <= str1[i] <= "Z") and\
        ("a" <= str1[i+1] <= "z" or "A" <= str1[i+1] <= "Z")):
            A.append(str1[i].lower() + str1[i+1].lower())

    for i in range(len(str2)-1):
        if (("a" <= str2[i] <= "z" or "A" <= str2[i] <= "Z") and\
        ("a" <= str2[i+1] <= "z" or "A" <= str2[i+1] <= "Z")):
            B.append(str2[i].lower() + str2[i+1].lower())

    sum_of_AB = multiset_sum(A, B)
    intersection = multiset_intersection(A, B)
    
    if (len(sum_of_AB) == 0) and (len(intersection) == 0):
        return 65536
    if (len(sum_of_AB) >= 0) and (len(intersection) == 0):
        return 0
    
    answer = ((len(intersection) / len(sum_of_AB)))
    
    return int(answer * 65536)