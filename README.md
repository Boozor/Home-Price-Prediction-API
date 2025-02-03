# Home-Price-Prediction-API
Welcome to the Home Price Prediction API project! This Flask-based web application provides an API endpoint for predicting house prices based on various input features. The application supports both single and batch predictions, allowing you to input one or multiple records at a time.

This README provides detailed instructions on how to set up and run the application locally, how to use Docker to containerize and run the application, how to execute unit tests using `pytest`, and examples of how to interact with the API using `curl`.

## Table of Contents
* Prerequisites
* Project Structure
* Running the Application Locally
   * Setup Virtual Environment
   * Install Dependencies
   * Run the Application
* Running the Application with Docker
   * Build the Docker Image
   * Run the Docker Container
   * Access the Container's Shell
* Running Unit Tests
* Interacting with the API
   * API Endpoint Details
   * Sample Inputs
   * Using `curl` to Make Requests
      * Sending a Single Record
      * Sending Multiple Records
      * Using JSON Files
      * Using Inline JSON Data
* Notes
* License

## Prerequisites
Before you begin, ensure you have the following software installed on your system:

  * **Python 3**: The application is built using Python 3.11.11 and Python 3.12.4.
  * **pip**: Python package manager to install dependencies.
  * **virtualenv / venv**: For creating an isolated Python environment.
  * **Docker**: To build and run the application in a container.
  * **Git**: To clone the repository.

## Project Structure
```plaintext
├── app.py                  # Main Flask application
├── home_price_model.pkl    # Serialized machine learning model
├── features.json           # JSON file with expected input features and data types
├── requirements.txt        # Python dependencies
├── tests/                  # Directory containing unit tests
│   ├── __init__.py
│   └── test_app.py         # Unit test file for the application
├── inputs/                 # Directory containing sample input JSON files
│   ├── single_record_valid.json
│   ├── multiple_records_valid.json
│   ├── single_record_missing_fields.json
│   └── multiple_records_invalid_types.json
├── Dockerfile              # Dockerfile to build the Docker image
├── pytest.ini              # To ignore depreciation warning
└── README.md               # Project documentation (this file)
```
## Running the Application Locally
Follow the steps below to set up and run the application on your local machine.

### Setup Virtual Environment
1. **Create a Virtual Environment**:
   ```code
   python -m venv venv
   ```
2. **Activate the Virtual Environment**:
     * On Unix or Linux:
       ```code
       source venv/bin/activate
       ```
     * On Windows:
       ```code
       venv\Scripts\activate
       ```
### Install Dependencies
Install the required Python packages using `pip`:
```code
pip install -r requirements.txt
```
## Run the Application
Execute the Flask application:
```code
python app.py
```
The application will start running on `http://0.0.0.0:50505/`.

## Running the Application with Docker
You can containerize and run the application using Docker.

### Build the Docker Image
1. **Option 1: Build from Local Directory**:

Navigate to the project's root directory (where the `Dockerfile` is located) and run:
```code
docker build -t home-price-prediction-api .
```
2. **Option 2: Build Directly from GitHub (No Local Clone Required)**
```bash
docker build -t home-price-prediction-api https://github.com/Boozor/Home-Price-Prediction-API.git
```
**Notes**: Replace Boozor/Home-Price-Prediction-API.git with your repo URL if using a fork.

### Run the Docker Container
2. **Run the Docker Container**:
   ```code
   docker run -p 50505:50505 --name home-price-api home-price-prediction-api
   ```
   This command maps port `50505` in the container to port `50505` on your host machine.
   
The application will be accessible at `http://localhost:50505/`.

### Access the Container's Shell
You can access the shell of the running Docker container to run commands as you would in your local terminal. This is useful for debugging, running tests, or managing files within the container.
```code
docker exec -it home-price-api /bin/bash
```
**Example Usage**:
Once inside the container's shell, you can navigate the file system and execute commands for running unit tests, processing input files, and more, just like in a regular terminal session.
```bash
cd /app
ls -la
pytest tests/
```
To exit the container's shell, type `exit` or press `Ctrl + D`.

## Running Unit Tests
The project includes unit tests to ensure the application works as expected.

1. **Install Testing Dependencies**:
The `requirements.txt` file should already include `pytest`. If not, install it:
```code
pip install pytest
```
2. **Run the Unit Tests**:
From the project's root directory, run:
```code
pytest tests/
```
This command will discover and execute all tests in the `tests/` directory.

## Interacting with the API
### API Endpoint Details
* **Main Endpoint (Health Check)**:
  * URL: `http://localhost:50505/`
  * Method: GET
  * Description: Returns a welcome message indicating the API is running.

* **Prediction Endpoint**:
  * URL: `http://localhost:50505/predict`
  * Method: POST
  * Content-Type: application/json
  * Description: Accepts JSON input and returns house price predictions.

### Sample Inputs
Sample input JSON files are provided in the inputs/ directory:
* Single Valid Record: `inputs/single_record_valid.json`
* Multiple Valid Records: `inputs/multiple_records_valid.json`
* Single Record Missing Fields: `inputs/single_record_missing_fields.json`
* Multiple Records with Invalid Types: `inputs/multiple_records_invalid_types.json`

## Using `curl` to Make Requests
You can use `curl` to interact with the API endpoints.

**Sending a Single Record**

**Option 1: Using a JSON File**

Assuming you have a file `inputs/single_record_valid.json` containing:
```json
{
  "LotArea": 8450,
  "YearBuilt": 2003,
  "1stFlrSF": 856,
  "2ndFlrSF": 854,
  "FullBath": 2,
  "BedroomAbvGr": 3,
  "TotRmsAbvGrd": 8
}
```
**Command**:
```code
curl -X POST http://localhost:50505/predict \
     -H "Content-Type: application/json" \
     -d @inputs/single_record_valid.json
```

**Option 2: Using Inline JSON Data**
```code
curl -X POST http://localhost:50505/predict \
     -H "Content-Type: application/json" \
     -d '{
       "LotArea": 8450,
       "YearBuilt": 2003,
       "1stFlrSF": 856,
       "2ndFlrSF": 854,
       "FullBath": 2,
       "BedroomAbvGr": 3,
       "TotRmsAbvGrd": 8
     }'
```

**Sending Multiple Records**

**Option 1: Using a JSON File**

Assuming you have a file `inputs/multiple_records_valid.json` containing:
```json
[
  {
    "LotArea": 7500,
    "YearBuilt": 2010,
    "1stFlrSF": 920,
    "2ndFlrSF": 880,
    "FullBath": 2,
    "BedroomAbvGr": 4,
    "TotRmsAbvGrd": 9
  },
  {
    "LotArea": 6200,
    "YearBuilt": 1998,
    "1stFlrSF": 780,
    "2ndFlrSF": 760,
    "FullBath": 1,
    "BedroomAbvGr": 3,
    "TotRmsAbvGrd": 7
  }
]
```
**Command**:
```code
curl -X POST http://localhost:50505/predict \
     -H "Content-Type: application/json" \
     -d @inputs/multiple_records_valid.json
```
**Option 2: Using Inline JSON Data**
```code
curl -X POST http://localhost:50505/predict \
     -H "Content-Type: application/json" \
     -d '[
  {
    "LotArea": 7500,
    "YearBuilt": 2010,
    "1stFlrSF": 920,
    "2ndFlrSF": 880,
    "FullBath": 2,
    "BedroomAbvGr": 4,
    "TotRmsAbvGrd": 9
  },
  {
    "LotArea": 6200,
    "YearBuilt": 1998,
    "1stFlrSF": 780,
    "2ndFlrSF": 760,
    "FullBath": 1,
    "BedroomAbvGr": 3,
    "TotRmsAbvGrd": 7
  }
]'
```

## Notes
* **Input Validation**: The API validates inputs for missing fields, data types, and value ranges. If any record fails validation, the API returns an error message indicating the issue.
* **Batch Predictions**: The `/predict` endpoint supports batch predictions. You can send a list of records, and the API will return a list of predictions.
* **Response Format**:
  * **Success**: Returns a JSON object with `success: true` and a `predictions` list.
  * **Error**: Returns a JSON object with `success: false` and an `error` message.

**Example Successful Response:**

Single Record:
```json
{
  "success": true,
  "predictions": [205680.26315789475]
}
```
Multiple Records:
```json
{
  "success": true,
  "predictions": [250000.0, 200000.0]
}
```

## License
This project is licensed under the MIT License.
