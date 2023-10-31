def get_dict_value(to_scheme, rep_d, key):
    val = rep_d.get(key, key)
    if type(val) is dict:
        return val[to_scheme]
    return val
