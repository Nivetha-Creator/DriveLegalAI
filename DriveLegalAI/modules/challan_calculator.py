import json


def calculate_challan(
    country,
    state,
    vehicle,
    violation,
    offense_count=0
):

    with open("data/traffic_rules.json", "r") as file:
        rules = json.load(file)

    for rule in rules:

        if (
            rule["country"].lower() == country.lower()
            and rule["state"].lower() == state.lower()
            and rule["vehicle"].lower() == vehicle.lower()
            and rule["violation"].lower() == violation.lower()
        ):

            base_fine = int(rule["fine"])

            # Repeat Offense Logic
            if offense_count == 0:
                calculated_fine = base_fine

            elif offense_count == 1:
                calculated_fine = base_fine * 2

            elif offense_count == 2:
                calculated_fine = base_fine * 3

            else:
                calculated_fine = base_fine * 4

            return {
                "country": rule["country"],
                "state": rule["state"],
                "vehicle": rule["vehicle"],
                "violation": rule["violation"],
                "law": rule["law"],
                "description": rule["description"],
                "fine": rule["fine"],
                "calculated_fine": calculated_fine,
                "offense_count": offense_count
            }

    return None