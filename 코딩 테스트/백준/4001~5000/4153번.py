# backjoon
while True:
    _list = list(map(int, input().split()))
    _list = sorted(_list)

    if _list[0] == 0:
        break
    
    if (_list[0] ** 2 + _list[1] ** 2) == _list[2] ** 2:
        print("right")
    else:
        print("wrong")