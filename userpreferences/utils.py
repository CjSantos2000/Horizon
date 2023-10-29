import json


def get_currencies_from_json(file_path):
    currency_data = []

    with open(file_path, "r") as json_file:
        data = json.load(json_file)

        for key, value in data.items():
            currency_data.append({"name": key, "value": value})

    return currency_data
