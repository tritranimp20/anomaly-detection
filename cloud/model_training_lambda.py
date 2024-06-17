# Model Training in Cloud

import boto3
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.svm import OneClassSVM
import joblib
import os

def lambda_handler(event, context):
    # Initialize S3 client
    s3 = boto3.client('s3')

    # Define S3 bucket and file names
    bucket_name = 'bkimp-ads'
    processed_data_file = 'data/processed/preprocessed_data.csv'
    labels_file = 'data/processed/labels.csv'
    iso_forest_model_file = 'model/iso_forest_model.pkl'
    svm_model_file = 'model/svm_model.pkl'
    rf_model_file = 'model/rf_model.pkl'

    # Read processed data from S3
    processed_data_obj = s3.get_object(Bucket=bucket_name, Key=processed_data_file)
    labels_obj = s3.get_object(Bucket=bucket_name, Key=labels_file)

    X = pd.read_csv(processed_data_obj['Body'])
    y = pd.read_csv(labels_obj['Body'])

    # Train Isolation Forest
    iso_forest = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
    iso_forest.fit(X)

    # Train One-Class SVM
    svm = OneClassSVM(kernel='rbf', gamma=0.1, nu=0.01)
    svm.fit(X)

    # Train Random Forest Classifier
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y.values.ravel())

    # Save models to temporary local storage
    joblib.dump(iso_forest, '/tmp/iso_forest_model.pkl')
    joblib.dump(svm, '/tmp/svm_model.pkl')
    joblib.dump(rf, '/tmp/rf_model.pkl')

    # Upload models to S3
    s3.upload_file('/tmp/iso_forest_model.pkl', bucket_name, iso_forest_model_file)
    s3.upload_file('/tmp/svm_model.pkl', bucket_name, svm_model_file)
    s3.upload_file('/tmp/rf_model.pkl', bucket_name, rf_model_file)

    # Clean up local temporary files
    os.remove('/tmp/iso_forest_model.pkl')
    os.remove('/tmp/svm_model.pkl')
    os.remove('/tmp/rf_model.pkl')

    return {
        'statusCode': 200,
        'body': 'Model training completed and models uploaded to S3'
    }

if __name__ == '__main__':
    lambda_handler(None, None)
