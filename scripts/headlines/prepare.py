import os
import json
import pandas as pd


def prepare_volunteers():
    shifts = pd.read_csv('data/metrics/volunteers/shifts.csv')
    result = {
        'shifts': int(shifts.attended.sum()),
        'hours': int(shifts.volunteer_hours.sum().round()),
    }
    return result


if __name__ == "__main__":
    volunteers = prepare_volunteers()

    file_content = "export default " + json.dumps({
        'volunteers': volunteers
    }) + ";"

    os.makedirs('docs/_data/headlines/', exist_ok=True)
    with open('docs/_data/headlines/values.js', 'w') as file:
        file.write(file_content)
