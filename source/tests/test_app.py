import sys
import os
import pytest

# Add the project root directory to sys.path to ensure the 'app' module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # Import the Flask app from application

@pytest.fixture
def client():
    """
    Create a test client for the Flask app.

    This fixture sets up a test client that can be used to send requests to the Flask application
    without running the server.
    """
    app.config['TESTING'] = True  # Enable testing mode
    with app.test_client() as client:
        yield client  # Provide the test client to the test functions

def test_hello_endpoint(client):
    """
    Test the root endpoint ('/') to ensure it returns the expected JSON response.

    Sends a GET request to the '/' endpoint and asserts that the response status code is 200
    and that the response JSON matches the expected value.
    """
    response = client.get('/')  # Send a GET request to the root endpoint
    assert response.status_code == 200  # Expect a 200 OK status code
    assert response.json == {"success": True, "message": "Hello, World!"}  # Check the response JSON content

def test_predict_endpoint_valid_input(client):
    """
    Test the '/predict' endpoint with valid input data.

    Sends a POST request with valid JSON input and verifies that the response contains predictions.
    """
    input_data = {
        "LotArea": 8450,
        "YearBuilt": 2003,
        "1stFlrSF": 856,
        "2ndFlrSF": 854,
        "FullBath": 2,
        "BedroomAbvGr": 3,
        "TotRmsAbvGrd": 8
    }
    # Send a POST request with valid input data
    response = client.post('/predict', json=input_data)
    assert response.status_code == 200  # Expect a 200 OK status code
    # Updated to check for 'predictions' key
    assert "predictions" in response.json  # Check that 'predictions' is in the response
    # Extract the predictions list
    predictions = response.json["predictions"]
    # Ensure that the predictions list is not empty and contains one prediction
    assert isinstance(predictions, list), "Predictions should be a list"
    assert len(predictions) == 1, "There should be one prediction in the list"
    assert isinstance(predictions[0], (int, float)), "Prediction should be a numeric value"

def test_predict_endpoint_missing_input(client):
    """
    Test the '/predict' endpoint with missing input data.

    Sends a POST request with an empty JSON object and verifies that the application
    returns an error indicating that required fields are missing.
    """
    input_data = {}  # Empty input data
    # Send a POST request with empty input data
    response = client.post('/predict', json=input_data)
    assert response.status_code == 400  # Expect a 400 Bad Request status code
    assert "error" in response.json  # Check that 'error' is in the response
    # Update the expected error message to match the actual application response
    expected_error_message = (
        "Record 0: Missing required fields: ['LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF', "
        "'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd']"
    )
    assert response.json["error"] == expected_error_message  # Check the error message

def test_predict_endpoint_invalid_input(client):
    """
    Test the '/predict' endpoint with invalid input data types.

    Sends a POST request where one of the fields has an invalid data type and verifies that the
    application returns an error indicating invalid input format.
    """
    input_data = {
        "LotArea": "eighty_four_fifty",  # Invalid data type (string instead of integer)
        "YearBuilt": 2003,
        "1stFlrSF": 856,
        "2ndFlrSF": 854,
        "FullBath": 2,
        "BedroomAbvGr": 3,
        "TotRmsAbvGrd": 8
    }
    # Send a POST request with invalid input data
    response = client.post('/predict', json=input_data)
    assert response.status_code == 400  # Expect a 400 Bad Request status code
    assert "error" in response.json  # Check that 'error' is in the response
    assert "Invalid input format" in response.json["error"]  # Check that the error message indicates invalid input format

def test_predict_endpoint_missing_fields(client):
    """
    Test the '/predict' endpoint with missing required fields.

    Sends a POST request missing some of the required fields and verifies that the
    application returns an error indicating which fields are missing.
    """
    input_data = {
        "LotArea": 8450,
        "YearBuilt": 2003
        # Missing other required fields: "1stFlrSF", "2ndFlrSF", "FullBath", "BedroomAbvGr", "TotRmsAbvGrd"
    }
    # Send a POST request with missing fields
    response = client.post('/predict', json=input_data)
    assert response.status_code == 400  # Expect a 400 Bad Request status code
    assert "Missing required fields" in response.json["error"]  # Check that the error indicates missing fields

def test_predict_endpoint_extra_fields(client):
    """
    Test the '/predict' endpoint with extra, unexpected fields in the input data.

    Sends a POST request with extra fields not expected by the model and verifies that the
    application returns an error indicating unexpected fields.
    """
    input_data = {
        "LotArea": 8450,
        "YearBuilt": 2003,
        "1stFlrSF": 856,
        "2ndFlrSF": 854,
        "FullBath": 2,
        "BedroomAbvGr": 3,
        "TotRmsAbvGrd": 8,
        "ExtraField": "invalid"  # Unexpected field
    }
    # Send a POST request with extra fields
    response = client.post('/predict', json=input_data)
    assert response.status_code == 400  # Expect a 400 Bad Request status code
    assert "Unexpected fields provided" in response.json["error"]  # Check that the error indicates unexpected fields

def test_predict_endpoint_invalid_values(client):
    """
    Test the '/predict' endpoint with invalid values (e.g., negative numbers).

    Sends a POST request where one of the fields has an invalid value and verifies that the
    application returns an error indicating invalid values.
    """
    input_data = {
        "LotArea": -100,  # Invalid value (negative number)
        "YearBuilt": 2003,
        "1stFlrSF": 856,
        "2ndFlrSF": 854,
        "FullBath": 2,
        "BedroomAbvGr": 3,
        "TotRmsAbvGrd": 8
    }
    # Send a POST request with invalid values
    response = client.post('/predict', json=input_data)
    assert response.status_code == 400  # Expect a 400 Bad Request status code
    assert "Invalid values" in response.json["error"]  # Check that the error indicates invalid values

def test_predict_endpoint_bad_json_input(client):
    """
    Test the '/predict' endpoint with malformed JSON input.

    Sends a POST request with invalid JSON data and verifies that the application
    returns a JSON error response indicating invalid JSON input format.
    """
    # Malformed JSON input (missing comma between "FullBath" and "BedroomAbvGr")
    bad_json_data = '''
    {
        "LotArea": 8450,
        "YearBuilt": 2003,
        "1stFlrSF": 856,
        "2ndFlrSF": 854,
        "FullBath": 2
        "BedroomAbvGr": 3,
        "TotRmsAbvGrd": 8
    }
    '''  # Note the missing comma after "FullBath": 2

    # Send POST request with malformed JSON data
    response = client.post('/predict', data=bad_json_data, content_type='application/json')

    # Assert that the status code is 400 Bad Request
    assert response.status_code == 400  # The server should return 400 Bad Request

    # Assert that the response is in JSON format
    assert response.content_type == 'application/json'  # Response should be JSON

    # Parse the response JSON
    response_json = response.get_json()

    # Assert that the response indicates a failure
    assert response_json['success'] is False  # 'success' should be False

    # Assert that the error message indicates invalid JSON input
    assert response_json['error'] == 'Invalid JSON input format'  # Error should be about invalid JSON