from flask import Blueprint, jsonify, request
from app.services.receipt_services import generate_receipt_id, compute_rewards
from app.models.receipt_model import validate_receipt_data, validate_receipt_boundaries
from jsonschema import validate, ValidationError

receipt_routes = Blueprint("receipt_routes", __name__)

@receipt_routes.route('/receipts/process', methods=['POST'])
def process_receipt():
    try:
        if not request.is_json:
            return jsonify({"msg": "Receipt is invalid"}), 400

        data = request.get_json()

        # Validate the request data
        validate_receipt_data(data)

        #Validate the data parameters
        bln, msg = validate_receipt_boundaries(data)
        if not bln:
            return jsonify({"msg": msg}), 400

        # Call the service to process the receipt
        response, status_code = generate_receipt_id(data)
        return jsonify(response), status_code

    except ValidationError as e:
        # Return validation errors
        return jsonify({"msg": "Receipt is invalid from validator"}), 400

    except Exception as e:
        return jsonify({"msg": str(e)}), 400


@receipt_routes.route('/receipts/<id>/points', methods=['GET'])
def get_reward_points(id):
    try:
        response, status_code = compute_rewards(id)
        print(response, status_code)
        return response

    except Exception as e:
        return jsonify({"msg": str(e)}), 400
