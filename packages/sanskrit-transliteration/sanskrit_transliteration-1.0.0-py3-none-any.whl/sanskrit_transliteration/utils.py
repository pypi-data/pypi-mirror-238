def get_dict_value(
        to_scheme: str,
        rep_d: dict[str, str | dict[str, str]],
        key: str
) -> str:
    """
    If value in dict is also a dict then the key will identify the scheme.
    If not return char
    :param to_scheme: any string
    :param rep_d: dict with a string as key and a string or dict as value
    :param key: any string value
    """
    val = rep_d.get(key, key)
    if type(val) is dict:
        return val[to_scheme]
    return val
