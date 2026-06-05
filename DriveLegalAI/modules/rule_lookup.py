import json


def get_rules_by_state(country, state):

    with open("data/traffic_rules.json", "r") as file:
        rules = json.load(file)

    filtered_rules = []

    for rule in rules:

        if (
            rule["country"].lower() == country.lower()
            and rule["state"].lower() == state.lower()
        ):

            filtered_rules.append(rule)

    return filtered_rules