# anomaly_detection.py
import pandas as pd
import joblib
import argparse
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report

def preprocess_new_data(new_data, columns, imputer, scaler):
    # Preprocess the new data
    new_data['timestamp'] = pd.to_datetime(new_data['timestamp'])
    new_data['protocol'] = new_data['protocol'].map({'TCP': 6, 'UDP': 17})  # Convert protocols to numeric values
    new_data['bytes'] = new_data['bytes'].astype(int)
    new_data['src_port'] = new_data['src_port'].astype(int)
    new_data['dst_port'] = new_data['dst_port'].astype(int)
    new_data.ffill(inplace=True)  # Forward fill missing values

    # Convert 'protocol' to numeric using one-hot encoding
    new_data = pd.get_dummies(new_data, columns=['protocol'])

    # Ensure all columns are present
    for col in columns:
        if col not in new_data.columns:
            new_data[col] = 0

    # Reorder columns to match the training data
    X_new = new_data[columns]

    # Impute missing values
    X_new = imputer.transform(X_new)

    # Normalize numerical features using StandardScaler
    X_new = scaler.transform(X_new)

    return pd.DataFrame(X_new, columns=columns)

def perform_anomaly_detection(new_data_file, output_file, iso_forest_file, svm_file, rf_file, labels_file, columns_file, imputer_file, scaler_file):
    # Load the models
    iso_forest = joblib.load(iso_forest_file)
    svm = joblib.load(svm_file)
    rf = joblib.load(rf_file)
    columns = joblib.load(columns_file)
    imputer = joblib.load(imputer_file)
    scaler = joblib.load(scaler_file)

    # Load new data for anomaly detection (assuming the same structure as the training data, but without the 'label' column)
    new_data = pd.read_csv(new_data_file)
    y_true = pd.read_csv(labels_file)['label']  # Load true labels for comparison

    # Preprocess the new data
    X_new = preprocess_new_data(new_data, columns, imputer, scaler)

    # Perform anomaly detection
    iso_forest_predictions = iso_forest.predict(X_new)
    svm_predictions = svm.predict(X_new)
    rf_predictions = rf.predict(X_new)

    # Convert Isolation Forest and SVM predictions from -1/1 to 0/1
    iso_forest_predictions = [1 if x == -1 else 0 for x in iso_forest_predictions]
    svm_predictions = [1 if x == -1 else 0 for x in svm_predictions]

    # Add predictions to the new data
    new_data['iso_forest_anomaly'] = iso_forest_predictions
    new_data['svm_anomaly'] = svm_predictions
    new_data['rf_anomaly'] = rf_predictions

    # Save the results to a new CSV file
    new_data.to_csv(output_file, index=False)

    # Print classification reports for each model
    print("Isolation Forest Classification Report:\n", classification_report(y_true, iso_forest_predictions, zero_division=0))
    print("One-Class SVM Classification Report:\n", classification_report(y_true, svm_predictions, zero_division=0))
    print("Random Forest Classification Report:\n", classification_report(y_true, rf_predictions, zero_division=0))

    print(f"Anomaly detection completed. Results saved to '{output_file}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Perform anomaly detection using trained models.')
    parser.add_argument('--new_data_file', type=str, default='data/new_network_traffic_data.csv', help='Input CSV file with new data')
    parser.add_argument('--output_file', type=str, default='data/anomaly_detection_results.csv', help='Output CSV file for anomaly detection results')
    parser.add_argument('--iso_forest_file', type=str, default='model/iso_forest_model.pkl', help='File to load the Isolation Forest model')
    parser.add_argument('--svm_file', type=str, default='model/svm_model.pkl', help='File to load the One-Class SVM model')
    parser.add_argument('--rf_file', type=str, default='model/rf_model.pkl', help='File to load the Random Forest model')
    parser.add_argument('--labels_file', type=str, default='data/test_labels.csv', help='CSV file with true labels for the test data')
    parser.add_argument('--columns_file', type=str, default='model/columns.pkl', help='File to load the column names')
    parser.add_argument('--imputer_file', type=str, default='model/imputer.pkl', help='File to load the imputer')
    parser.add_argument('--scaler_file', type=str, default='model/scaler.pkl', help='File to load the scaler')
    args = parser.parse_args()

    perform_anomaly_detection(args.new_data_file, args.output_file, args.iso_forest_file, args.svm_file, args.rf_file, args.labels_file, args.columns_file, args.imputer_file, args.scaler_file)
