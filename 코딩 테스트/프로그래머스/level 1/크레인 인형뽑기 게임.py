def solution(board, moves):
    basket = []
    pop_dolls = 0


    for j in range(len(moves)):
        take = moves[j] - 1
        for i in range(len(board)):
            if board[i][take] == 0:
                continue
            
            basket.append(board[i][take])
            board[i][take] = 0
            if len(basket) >= 2 and basket[-1] == basket[-2]:
                pop_dolls += 2
                basket.pop()
                basket.pop()
            
            break

    return pop_dolls