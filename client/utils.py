
def merge_dictionaries(*dictionaries: dict):
    arr_len = len(dictionaries)
    if arr_len == 0:
        return {}
    if arr_len == 1:
        return dictionaries[0]
    ret = dictionaries[0].copy()
    for i in range(1, arr_len):
        ret.update(dictionaries[i])
    return ret
