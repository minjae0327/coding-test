def solution(video_len, pos, op_start, op_end, commands):
    minute, second = pos.split(":")
    pos = int(minute + second)

    minute, second = video_len.split(":")
    video_len = int(minute + second)

    minute, second = op_start.split(":")
    op_start = int(minute + second)

    minute, second = op_end.split(":")
    op_end = int(minute + second)
    
    if op_start < pos < op_end:
            pos = op_end

    for command in commands:
        if command == "next":
            pos += 10
            if pos % 100 >= 60:
                pos += 40
            
            if pos > video_len:
                pos = video_len
        else:
            pos -= 10
            if pos % 100 >= 90:
                pos -= 40
                
            if pos < 0:
                pos = 0
         
        if op_start <= pos < op_end:
            pos = op_end
        
    pos = str(pos)
    while (len(pos) < 4):
        pos = "0" + pos
    minute = pos[:2]
    second = pos[2:]
    
    return minute + ":" + second