from flask import jsonify
from jsonschema import validate, ValidationError
import yaml
import datetime
import re
from flask import current_app as app

def validate_receipt_data(data):
    with open("receipt_api.yml", "r") as schema_file:
        schema = yaml.safe_load(schema_file)

        validate(instance=data, schema=schema)




def validate_receipt_boundaries(data):
    '''
    Ip: JSON object
    ret: Boolean, message
    I am returning specific error messages based on type of error
    isntead of standard error message.
    The API error message is standard (given in the api.yml on github)
    '''
    # Check 1: Check date format
    date_pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(date_pattern, data['purchaseDate']):
        return False, "date check failed"

    # Check 2: Check date range
    try:
        date_format = '%Y-%m-%d'
        date_object = datetime.datetime.strptime(data['purchaseDate'], date_format)
    except ValueError:
        return False, "date range check failed"

    # Check 3: Check Time Format and range
    time_pattern = r"^\d{2}:\d{2}$"
    if not re.match(time_pattern, data['purchaseTime']):
        return False, "time regex check failed"
    time_value = data['purchaseTime'].split(":")
    if not (0 <= int(time_value[0]) < 24 and 0 <= int(time_value[1]) < 60):
        return False, "Time range check failed"

    # Check 3: Check min items
    # Done by yml validator

    # Check 4: regex for description
    # Done by yml validator

    # Check 5: negative prices and negative total
    # Done by yml regex validator

    # Check 6: Check total equals sum of prices
    tmp = 0.00
    for item in data["items"]:
        tmp += round(float(item["price"]), 2)
    if round(tmp, 2) != round(float(data["total"]), 2):
        return False, "Sum of prices doesn't match total"

    else:
        return True, "All cases passed"
