

def clean_pdf_list(param):
    if param:
        param = [p['path'] for p in param]
    return param


def clean_pdf(param):
    if param:
        param = param[0]['path']
    return param


def clean_latitude(param):
    north = 1 if 'N' in param[-1] else -1
    degrees = int(param[:2], 10)
    minutes = int(param[3:5], 10)
    if "." in param:
        # seconds is a float
        seconds = int(param[6:-4], 10)
    else:
        seconds = int(param[6:-2], 10)
    return (seconds + 60 * minutes + 3600 * degrees) * north


def clean_longitude(param):
    east = 1 if 'E' in param[-1] else -1
    degrees = int(param[:3], 10)
    minutes = int(param[4:6], 10)
    if "." in param:
        # seconds is a float
        seconds = int(param[7:-4], 10)
    else:
        seconds = int(param[7:-2], 10)
    return (seconds + 60 * minutes + 3600 * degrees) * east
