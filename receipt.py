
import re
import math
import uuid
import yaml
import jsonschema
from jsonschema import validate
import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)


def boundry_check(data):
    '''
    Ip: JSON object
    ret: Boolean, message
    I am returning specific error messages based on type of error
    isntead of standard error message.
    The API error message is standard (given in the api.yml on github)
    '''
    #Check 1: Check date format
    date_pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(date_pattern, data['purchaseDate']):
        return False, "date check failed"
    
    #Check 2: Check date range
    try:
        date_format = '%Y-%m-%d'
        date_object = datetime.datetime.strptime(data['purchaseDate'], date_format)
    except ValueError:
        return False, "date range check failed"
    
    #Check 3: Check Time Format and range
    time_pattern = r"^\d{2}:\d{2}$"
    if not re.match(time_pattern, data['purchaseTime']):
        return False, "time regex check failed"
    time_value = data['purchaseTime'].split(":")
    if not (0<=int(time_value[0])<24 and 0<=int(time_value[1])<60):
        return False, "Time range check failed"
    
    #Check 3: Check min items
    # Done by yml validator

    #Check 4: regex for description
    # Done by yml validator

    #Check 5: negative prices and negative total
    # Done by yml regex validator

    #Check 6: Check total equals sum of prices
    tmp = 0.00
    for item in data["items"]:
        tmp += round(float(item["price"]),2)
    if round(tmp,2) != round(float(data["total"]),2):
        return False, "Sum of prices doesn't match total"

    else:
        return True, "All cases passed"
    

# Load the JSON schema from the YAML file
with open("receipt_api.yml", "r") as schema_file:
    schema = yaml.safe_load(schema_file)

#In mem db 
receipt_db = dict()


@app.route('/receipts/process', methods=['POST'])
def generate_id():
    '''
    Ip: Comes from POST request
    ret: HTTP response
    Takes in the POST request with JSON object for receipt.
    Performs all the sanity check and returns ID for the reciept.
    Saves the ID with Receipt Object in dict.
    '''
    try:
        if not request.is_json:
            return jsonify({"msg": "Receipt is invalid"}), 400

        data = request.get_json()

        # Validate the request data against the loaded schema
        validate(instance=data, schema=schema)

        #Checking all the boundary cases
        boolean, msg = boundry_check(data)
        if not boolean:   
            return jsonify({"msg": msg}), 400
        
        # If validation succeeds, we generate an ID 
        receipt_id = uuid.uuid4()
        receipt_db[str(receipt_id)] = data

        return jsonify({"id":receipt_id}), 200

    except jsonschema.exceptions.ValidationError as e:
        # Return validation errors
        return jsonify({"msg": "Receipt is invalid from validator"}), 400


@app.route('/receipts/<id>/points', methods=['GET'])
def computer_rewards(id):
    '''
    Ip: Id
    Ret: Points
    Funtion takes in the receipt id and generates points based on the reward logic.
    '''
    points = 0
    if id in list(receipt_db.keys()):
        recepit_details = receipt_db.get(id)

        #One point for every alphanumeric character in the retailer name.
        points += len(re.findall('[a-zA-Z0-9]',recepit_details["retailer"]))

        # 50 points if the total is a round dollar amount with no cents.
        if float(recepit_details["total"]).is_integer():
            points += 50

        # 25 points if the total is a multiple of 0.25.
        if float(recepit_details["total"]) % 0.25 == 0:
            points += 25

        # 5 points for every two items on the receipt.
        points += (len(recepit_details["items"])//2) * 5

        # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
        #is it rounded up to nearest integer or floor integer?? 
        #ROUNDUP means ceil... Round means to nearest
        for item in recepit_details["items"]:
            if len(item["shortDescription"].strip()) % 3 == 0:
                points += math.ceil(float(item["price"]) * 0.2)

        # 6 points if the day in the purchase date is odd.
        if int(recepit_details["purchaseDate"].split("-")[-1]) % 2 == 1:
            points+=6

        # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
        # check if 14 is valid
        if 14<=int(recepit_details["purchaseTime"].split(":")[0])<16:
            points += 10

        return jsonify({"points":points}), 200
    
    else:
        return jsonify({"msg": "No receipt found for that id"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)  # Listen on all network interfaces
