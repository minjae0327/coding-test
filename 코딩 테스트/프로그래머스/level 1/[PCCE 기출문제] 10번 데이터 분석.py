def solution(data, ext, val_ext, sort_by):
    ext_sort_dict = {
    "code":0,
    "date":1,
    "maximum":2,
    "remain":3
    }
        
    filtered_data = []

    for i in range(len(data)):
        loc = ext_sort_dict[ext]
        if data[i][loc] < val_ext:
            filtered_data.append(data[i])
            
    filtered_data = sorted(filtered_data, key=lambda x: x[ext_sort_dict[sort_by]])
    
    return filtered_data