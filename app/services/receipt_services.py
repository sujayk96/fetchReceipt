import re
import math
import uuid
from app.models.receipt_model import validate_receipt_boundaries
from flask import current_app as app
from flask import jsonify


def generate_receipt_id(data):

    receipt_id = uuid.uuid4()
    app.receipt_db[str(receipt_id)] = data

    return {"id": receipt_id}, 200


def compute_rewards(id):
    '''
    Ip: Id
    Ret: Points
    Funtion takes in the receipt id and generates points based on the reward logic.
    '''
    points = 0
    print(id)
    print("keys",list(app.receipt_db.keys()))
    if id in list(app.receipt_db.keys()):
        print("Found")
        if id in list(app.receipt_rewards.keys()):
            print("value Found")
            return jsonify({"points": app.receipt_rewards[id]}), 200
        print("Value Not found")
        recepit_details = app.receipt_db.get(id)

        # One point for every alphanumeric character in the retailer name.
        points += len(re.findall('[a-zA-Z0-9]', recepit_details["retailer"]))

        # 50 points if the total is a round dollar amount with no cents.
        if float(recepit_details["total"]).is_integer():
            points += 50

        # 25 points if the total is a multiple of 0.25.
        if float(recepit_details["total"]) % 0.25 == 0:
            points += 25

        # 5 points for every two items on the receipt.
        points += (len(recepit_details["items"]) // 2) * 5

        # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
        # is it rounded up to nearest integer or floor integer??
        # ROUNDUP means ceil... Round means to nearest
        for item in recepit_details["items"]:
            if len(item["shortDescription"].strip()) % 3 == 0:
                points += math.ceil(float(item["price"]) * 0.2)

        # 6 points if the day in the purchase date is odd.
        if int(recepit_details["purchaseDate"].split("-")[-1]) % 2 == 1:
            points += 6

        # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
        # check if 14 is valid
        if 14 <= int(recepit_details["purchaseTime"].split(":")[0]) < 16:
            points += 10

        app.receipt_rewards[id] = points
        return jsonify({"points": points}), 200

    else:
        return jsonify({"msg": "No receipt found for that id"}), 400
