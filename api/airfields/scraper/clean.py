def clean_map_name(param):
    return param.replace("_", " ")


def clean_category(param):
    return param.lower()


def clean_elevation(param):
    if param:
        return int(param[0], 10)
    return None

