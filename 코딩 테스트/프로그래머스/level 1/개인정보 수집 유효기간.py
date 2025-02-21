def process(y, m, dict, period):
    _m = m + dict[period]
    while _m > 12:
        y += 1
        _m -= 12
    
    return y, _m

def solution(today, terms, privacies):
    today = today.replace(".", "")
    dict_term = {}
    for _term in terms:
        condition, term = _term.split(" ")
        dict_term[condition] = int(term)
        
    destruction = []

    for i in range(len(privacies)):
        p_date, p_term = privacies[i].split(" ")    
        p_year, p_month, p_day = map(int, p_date.split("."))
        np_year, np_month, = process(p_year, p_month, dict_term, p_term)
        np_year, np_month, p_day = str(np_year), str(np_month), str(p_day)
        if len(np_month) == 1:
            np_month = "0" + np_month
        if len(p_day) == 1:
            p_day = "0" + p_day
        
        if  today >= np_year + np_month + p_day:
            destruction.append(i + 1)
    
    return destruction