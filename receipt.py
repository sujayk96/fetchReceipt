
import connexion
import re
import math
import uuid
import yaml
import jsonschema
from jsonschema import validate
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the JSON schema from the YAML file
with open("receipt_api.yml", "r") as schema_file:
    schema = yaml.safe_load(schema_file)

@app.route("/", methods= ['GET'])
def welcome():
  print("asdf")
  return "welcome to app!!"

receipt_db = dict()
@app.route('/receipts/process', methods=['POST'])
def generate_id():
    try:
        if not request.is_json:
            return jsonify({"msg": "Receipt is invalid"}), 400

        data = request.get_json()
        #print("schema is\n", schema)
        # Validate the request data against the loaded schema
        validate(instance=data, schema=schema)

        # If validation succeeds, process the request
        # ...
        receipt_id = uuid.uuid4()
        receipt_db[str(receipt_id)] = data

        # print("The data dictionry looks like follows!!!")
        # print(receipt_db)
        return jsonify({"id":receipt_id}), 200

        # return jsonify({"message": "JSON data is valid"}), 200
    except jsonschema.exceptions.ValidationError as e:
        # Return validation errors
        return jsonify({"msg": "Receipt is invalid"}), 400

   
    


@app.route('/receipts/<id>/points', methods=['GET'])
def computer_rewards(id):
    print("in compute function")
    points = 0
    if id in list(receipt_db.keys()):
        recepit_details = receipt_db.get(id)
        #One point for every alphanumeric character in the retailer name.
        points += len(re.findall('[a-zA-Z0-9]',recepit_details["retailer"]))
        print(points)
        # 50 points if the total is a round dollar amount with no cents.
        #print(float(recepit_details["total"]),"float value")
        if float(recepit_details["total"]).is_integer():
            points += 50
        print(points)
        # 25 points if the total is a multiple of 0.25.
        if float(recepit_details["total"]) % 0.25 == 0:
            points += 25

        print(points)
        # 5 points for every two items on the receipt.
        points += (len(recepit_details["items"])//2) * 5
        # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
        print(points)

        #is it rounded up to nearest integer or floor integer?? 
        #ROUNDUP means ceil... Round means to nearest
        for item in recepit_details["items"]:
            if len(item["shortDescription"].strip()) % 3 == 0:
                print(item["shortDescription"],float(item["price"]) * 0.2)
                #points += round(float(item["price"]) * 0.2)
                points += math.ceil(float(item["price"]) * 0.2)
        # 6 points if the day in the purchase date is odd.
            print(points)
        if int(recepit_details["purchaseDate"].split("-")[-1]) % 2 == 1:
            points+=6
        print(points)
        # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
        # check if 14 is valid
        if 14<=int(recepit_details["purchaseTime"].split(":")[0])<16:
            points += 10

        return jsonify({"points":points}), 200
    
    else:
        return jsonify({"msg": "No receipt found for that id"}), 400


if __name__ == '__main__':
    app.run(port=8001)