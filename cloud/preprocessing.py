# Preprocessing in Cloud

import boto3
import pandas as pd
from io import StringIO
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import joblib

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    # Define S3 bucket and file names
    bucket_name = 'bkimp-ads'
    raw_file_path = 'data/raw/training_network_traffic_data.csv'
    processed_file_path = 'data/processed/preprocessed_data.csv'
    columns_file_path = 'model/columns.pkl'
    imputer_file_path = 'model/imputer.pkl'
    scaler_file_path = 'model/scaler.pkl'

    # Read raw data from S3
    raw_obj = s3.get_object(Bucket=bucket_name, Key=raw_file_path)
    raw_data = pd.read_csv(raw_obj['Body'])

    # Handle missing values using forward fill method
    raw_data.ffill(inplace=True)

    # Convert 'protocol' to numeric using one-hot encoding
    raw_data = pd.get_dummies(raw_data, columns=['protocol'])

    # Prepare data for training
    X = raw_data.drop(columns=['timestamp', 'src_addr', 'dst_addr', 'action', 'log_status', 'label'])  # Exclude label from features
    
    # Save the columns
    columns = X.columns
    joblib.dump(columns, '/tmp/columns.pkl')
    s3.upload_file('/tmp/columns.pkl', bucket_name, columns_file_path)

    # Impute missing values for numeric data
    imputer = SimpleImputer(strategy='mean')
    X = imputer.fit_transform(X)
    joblib.dump(imputer, '/tmp/imputer.pkl')
    s3.upload_file('/tmp/imputer.pkl', bucket_name, imputer_file_path)

    # Normalize numerical features using StandardScaler
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    joblib.dump(scaler, '/tmp/scaler.pkl')
    s3.upload_file('/tmp/scaler.pkl', bucket_name, scaler_file_path)

    # Convert preprocessed data to DataFrame
    processed_data = pd.DataFrame(X, columns=columns)

    # Convert DataFrame to CSV
    csv_buffer = StringIO()
    processed_data.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=processed_file_path, Body=csv_buffer.getvalue())

    return {
        'statusCode': 200,
        'body': 'Data preprocessing completed and uploaded to S3'
    }