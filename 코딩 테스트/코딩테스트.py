def solution(n, words):
    game_round = 1
    counter = 0
    prev_word  = ''
    prev_words = []

    for word in words:
        counter += 1
        if len(prev_words) == 0:
            prev_word = word
            prev_words.append(prev_word)
            continue
        
        
        if prev_word[-1] != word[0] or (word in prev_words):
            return [counter, game_round]
            break
        elif prev_word[-1] == word[0]:
            prev_word = word
            prev_words.append(prev_word)
        if counter - n == 0:
            game_round += 1
            counter = 0  

    return [0, 0]