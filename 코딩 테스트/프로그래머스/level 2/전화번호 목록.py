def solution(phone_book):
    phone_book = sorted(phone_book)
    
    hash_table = {}

    for i in range(len(phone_book)):
        hash_table[phone_book[i]] = i
    
    for phone in phone_book:
        for i in range(1, len(phone)):
            prefix = phone[:i]
            
            if prefix in hash_table:
                return False
    
    return True