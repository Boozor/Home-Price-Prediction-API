from flask import Flask, jsonify, request
import logging
import joblib
import pandas as pd
import json
from werkzeug.exceptions import BadRequest

# Initialize Flask app
app = Flask(__name__)

# Set the logger level for Flask's logger
app.logger.setLevel(logging.INFO)

# Define the type mapping from strings to Python types
type_mapping = {
    "int": int,
    "float": float,
    "str": str,
}

# Load expected features from a JSON file
try:
    with open('features.json', 'r') as f:
        expected_features_str = json.load(f)
        # Convert string type names to Python types
        expected_features = {field: type_mapping[type_str] for field, type_str in expected_features_str.items()}
except FileNotFoundError:
    app.logger.error("features.json file not found. Please ensure it exists in the project directory.")
    raise SystemExit("features.json file is missing. Application cannot start without it.")
except Exception as e:
    app.logger.error(f"Error loading expected features: {str(e)}")
    raise SystemExit(e)

# Load the trained model
try:
    model = joblib.load('home_price_model.pkl')
except Exception as e:
    app.logger.error(f"Error loading model: {str(e)}")
    raise SystemExit(e)

@app.errorhandler(BadRequest)
def handle_bad_request(e):
    app.logger.error(f"BadRequest error: {str(e)}")
    # Check if the error is due to invalid JSON payload
    if "Failed to decode JSON object" in str(e) or "Expecting value" in str(e):
        return jsonify({"success": False, "error": "Invalid JSON input format"}), 400
    else:
        # Return the error description for other BadRequest errors
        return jsonify({"success": False, "error": str(e.description)}), e.code

@app.route('/')
def hello():
    app.logger.info('Main endpoint processing HTTP request')
    return jsonify({"success": True, "message": "Hello, World!"})

def validate_input_data(input_data_list, expected_features):
    """
    Validate each input record in the input data list for missing or extra fields and null values.
    """
    for idx, input_data in enumerate(input_data_list):
        if input_data is None:
            return False, f"Record {idx}: No input data provided"

        # Check for missing and extra fields
        missing_fields = [field for field in expected_features if field not in input_data]
        extra_fields = [field for field in input_data if field not in expected_features]

        if missing_fields:
            return False, f"Record {idx}: Missing required fields: {missing_fields}"

        if extra_fields:
            return False, f"Record {idx}: Unexpected fields provided: {extra_fields}"

        # Check for null values in required fields
        null_fields = [field for field in expected_features if input_data.get(field) is None]
        if null_fields:
            return False, f"Record {idx}: Fields cannot be null: {null_fields}"

    return True, ""

def check_data_types_and_values(input_data_list, expected_features):
    """
    Check data types and values of each input record in the input data list.
    """
    for idx, input_data in enumerate(input_data_list):
        type_errors = []
        invalid_values = []

        for field, expected_type in expected_features.items():
            value = input_data.get(field)
            if value is None:
                type_errors.append(f"Field '{field}' cannot be null")
                continue

            # Attempt to convert the value to the expected type
            try:
                original_value = value
                value = expected_type(value)
                input_data[field] = value  # Update input_data with the converted value

                # If the expected type is numeric, check if the value is non-negative
                if expected_type in [int, float] and value < 0:
                    invalid_values.append(f"Field '{field}' must be a non-negative number")
            except (ValueError, TypeError):
                type_errors.append(f"Field '{field}' must be of type {expected_type.__name__} (got value '{original_value}')")

        if type_errors:
            return False, f"Record {idx}: Invalid input format: Type errors - {', '.join(type_errors)}"

        if invalid_values:
            return False, f"Record {idx}: Invalid values: {', '.join(invalid_values)}"

    return True, ""

def convert_to_dataframe(input_data_list, expected_features):
    """
    Convert the list of validated input records to a pandas DataFrame.
    """
    try:
        # Create DataFrame with columns in the expected order
        input_df = pd.DataFrame(input_data_list, columns=expected_features.keys())
        return input_df, None
    except Exception as e:
        return None, str(e)

@app.route('/predict', methods=['POST'])
def predict():
    app.logger.info('Inference endpoint processing HTTP request')

    # Attempt to get JSON data from the request
    try:
        input_data = request.get_json()
        if input_data is None:
            raise BadRequest("No JSON input provided or invalid JSON format.")
    except BadRequest as e:
        app.logger.error(f"BadRequest exception: {str(e)}")
        return jsonify({"success": False, "error": "Invalid JSON input format"}), 400

    # Ensure input_data is a list
    if not isinstance(input_data, list):
        # If a single record is provided as a dictionary, wrap it in a list
        if isinstance(input_data, dict):
            input_data = [input_data]
        else:
            app.logger.error("Input data must be a list of records or a single record object.")
            return jsonify({"success": False, "error": "Input data must be a list of records or a single record object."}), 400

    # Step 1: Validate input data for missing or extra fields
    is_valid, error_message = validate_input_data(input_data, expected_features)
    if not is_valid:
        app.logger.error(f"Input validation error: {error_message}")
        return jsonify({"success": False, "error": error_message}), 400

    # Step 2: Check data types and values
    is_valid, error_message = check_data_types_and_values(input_data, expected_features)
    if not is_valid:
        app.logger.error(f"Data type/value validation error: {error_message}")
        return jsonify({"success": False, "error": error_message}), 400

    # Step 3: Convert the input data to a DataFrame
    input_df, error = convert_to_dataframe(input_data, expected_features)
    if error:
        app.logger.error(f"Error converting input data to DataFrame: {error}")
        return jsonify({"success": False, "error": f"Invalid input format: {error}"}), 400

    # Step 4: Perform prediction using the loaded model
    try:
        predictions = model.predict(input_df)
        app.logger.info(f"Predictions made successfully: {predictions.tolist()}")
        return jsonify({"success": True, "predictions": predictions.tolist()})
    except Exception as e:
        app.logger.error(f"Error making predictions: {str(e)}")
        return jsonify({"success": False, "error": f"Prediction failed: {str(e)}"}), 500

if __name__ == '__main__':
    # Run the Flask app on host 0.0.0.0 and port 50505
    app.run(debug=True, host='0.0.0.0', port=50505)