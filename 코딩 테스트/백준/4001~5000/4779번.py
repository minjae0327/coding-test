while True:
    try:
        n = int(input())

        length = pow(3, n)
        cantor = "-" * length

        def recursive(lines, length):
            if length == 1:
                return lines
            
            length = length // 3
            
            a = recursive(lines[:length], length)
            b = recursive(lines[length*2:], length)
            
            return a + " " * length + b

        cutted = recursive(cantor, length)
        print(cutted)
    except:
        break