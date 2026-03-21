def clean_data(data):

    clean = {}

    for key, value in data.items():
        if value >= 0:
            clean[key] = round(value, 2)

    return clean