import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
import joblib

def load_data(file_path):
    """Load dataset from a CSV file and return a DataFrame."""
    data = pd.read_csv(file_path)
    return data

def preprocess_data(data):
    """Extract relevant features and target variable for training."""
    features = ['LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd']
    X = data[features]  # Feature matrix
    y = data['SalePrice']  # Target variable
    return X, y

def find_best_tree_size(X_train, y_train, X_val, y_val):
    """Find the optimal max_leaf_nodes for Decision Tree Regressor by comparing MAE values."""
    best_size = None
    best_mae = float("inf")
    # Iterate through different max_leaf_nodes values to find the best one
    for max_leaf_nodes in [5, 25, 50, 100, 250, 500, 5000]:
        model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=1)
        model.fit(X_train, y_train)
        predictions = model.predict(X_val)
        mae = mean_absolute_error(y_val, predictions)
        if mae < best_mae:
            best_mae = mae
            best_size = max_leaf_nodes
    return best_size

def train_model(X_train, y_train, best_leaf_nodes):
    """Train a Decision Tree model using the optimal max_leaf_nodes."""
    model = DecisionTreeRegressor(max_leaf_nodes=best_leaf_nodes, random_state=1)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_val, y_val):
    """Evaluate the trained model using Mean Absolute Error (MAE)."""
    predictions = model.predict(X_val)
    mae = mean_absolute_error(y_val, predictions)
    return mae

def main():
    """Main function to execute the model training pipeline."""
    file_path = "home_price_data.csv"  # Update with actual path if needed
    
    # Load and preprocess data
    data = load_data(file_path)
    X, y = preprocess_data(data)
    
    # Split data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, random_state=1, test_size=0.2)
    
    # Find the optimal number of leaf nodes for the Decision Tree
    best_leaf_nodes = find_best_tree_size(X_train, y_train, X_val, y_val)
    
    # Train the model using the best leaf node size
    model = train_model(X_train, y_train, best_leaf_nodes)
    
    # Evaluate the model
    mae = evaluate_model(model, X_val, y_val)
    
    # Print results
    print(f"Optimal max_leaf_nodes: {best_leaf_nodes}")
    print(f"Model Evaluation - Mean Absolute Error: {mae}")
    
    # Save the trained model
    
    joblib.dump(model, 'home_price_model.pkl')
    print("Model saved as 'home_price_model.pkl'")

if __name__ == "__main__":
    main()
