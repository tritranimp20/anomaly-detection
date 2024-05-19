# preprocessing.py
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import os
import argparse
import joblib

def preprocess_data(input_file, output_file_data, output_file_labels, output_columns_file, imputer_file, scaler_file):
    # Ensure the 'data' directory exists
    os.makedirs('data', exist_ok=True)
    os.makedirs('model', exist_ok=True)

    # Load preprocessed data from local CSV file
    data = pd.read_csv(input_file)

    # Handle missing values using forward fill method
    data.ffill(inplace=True)

    # Convert 'protocol' to numeric using one-hot encoding
    data = pd.get_dummies(data, columns=['protocol'])

    # Prepare data for training
    X = data.drop(columns=['timestamp', 'src_addr', 'dst_addr', 'action', 'log_status', 'label'])  # Exclude label from features
    y = data['label']

    # Save the columns
    columns = X.columns
    joblib.dump(columns, output_columns_file)

    # Impute missing values for numeric data
    imputer = SimpleImputer(strategy='mean')
    X = imputer.fit_transform(X)
    joblib.dump(imputer, imputer_file)

    # Normalize numerical features using StandardScaler
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    joblib.dump(scaler, scaler_file)

    # Save the preprocessed data for model training
    pd.DataFrame(X, columns=columns).to_csv(output_file_data, index=False)

    print("Preprocessing completed. Preprocessed data saved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Preprocess network traffic data.')
    parser.add_argument('--input_file', type=str, default='data/network_traffic_data.csv', help='Input CSV file with raw data')
    parser.add_argument('--output_file_data', type=str, default='data/preprocessed_data.csv', help='Output CSV file for preprocessed data')
    parser.add_argument('--output_file_labels', type=str, default='data/labels.csv', help='Output CSV file for labels')
    parser.add_argument('--output_columns_file', type=str, default='model/columns.pkl', help='Output file for saving column names')
    parser.add_argument('--imputer_file', type=str, default='model/imputer.pkl', help='File to save the imputer')
    parser.add_argument('--scaler_file', type=str, default='model/scaler.pkl', help='File to save the scaler')
    args = parser.parse_args()

    preprocess_data(args.input_file, args.output_file_data, args.output_file_labels, args.output_columns_file, args.imputer_file, args.scaler_file)
