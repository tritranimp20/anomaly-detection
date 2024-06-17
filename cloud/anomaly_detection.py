# Anomaly Detection in Cloud

import boto3
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.svm import OneClassSVM
from sklearn.metrics import classification_report
from io import StringIO
import joblib

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    # Define S3 bucket and file names
    bucket_name = 'bkimp-ads'
    new_data_file_path = 'data/raw/testing_network_traffic_data.csv'
    processed_file_path = 'data/processed/preprocessed_data.csv'
    results_file_path = 'result/anomaly_detection_results.csv'
    imputer_file_path = 'model/imputer.pkl'
    scaler_file_path = 'model/scaler.pkl'
    rf_model_file_path = 'model/rf_model.pkl'
    if_model_file_path = 'model/if_model.pkl'
    svm_model_file_path = 'model/svm_model.pkl'

    # Read new data from S3
    new_data_obj = s3.get_object(Bucket=bucket_name, Key=new_data_file_path)
    new_data = pd.read_csv(new_data_obj['Body'])

    # Read preprocessed data from S3
    processed_obj = s3.get_object(Bucket=bucket_name, Key=processed_file_path)
    processed_data = pd.read_csv(processed_obj['Body'])

    # Read imputer and scaler from S3
    imputer_obj = s3.get_object(Bucket=bucket_name, Key=imputer_file_path)
    with open('/tmp/imputer.pkl', 'wb') as f:
        f.write(imputer_obj['Body'].read())
    imputer = joblib.load('/tmp/imputer.pkl')

    scaler_obj = s3.get_object(Bucket=bucket_name, Key=scaler_file_path)
    with open('/tmp/scaler.pkl', 'wb') as f:
        f.write(scaler_obj['Body'].read())
    scaler = joblib.load('/tmp/scaler.pkl')

    # Read models from S3
    rf_model_obj = s3.get_object(Bucket=bucket_name, Key=rf_model_file_path)
    with open('/tmp/rf_model.pkl', 'wb') as f:
        f.write(rf_model_obj['Body'].read())
    rf_model = joblib.load('/tmp/rf_model.pkl')

    if_model_obj = s3.get_object(Bucket=bucket_name, Key=if_model_file_path)
    with open('/tmp/if_model.pkl', 'wb') as f:
        f.write(if_model_obj['Body'].read())
    if_model = joblib.load('/tmp/if_model.pkl')

    svm_model_obj = s3.get_object(Bucket=bucket_name, Key=svm_model_file_path)
    with open('/tmp/svm_model.pkl', 'wb') as f:
        f.write(svm_model_obj['Body'].read())
    svm_model = joblib.load('/tmp/svm_model.pkl')

    # Prepare data for prediction
    X_new = new_data.drop(columns=['timestamp', 'src_addr', 'dst_addr', 'action', 'log_status', 'label'])
    X_new = imputer.transform(X_new)
    X_new = scaler.transform(X_new)

    # Perform anomaly detection
    new_data['iso_forest_anomaly'] = if_model.predict(X_new)
    new_data['svm_anomaly'] = svm_model.predict(X_new)
    new_data['rf_anomaly'] = rf_model.predict(X_new)

    # Generate classification report for each model
    y_true = new_data['label']  # Assuming 'label' column exists in new_data for true labels
    y_pred_if = new_data['iso_forest_anomaly']
    y_pred_svm = new_data['svm_anomaly']
    y_pred_rf = new_data['rf_anomaly']

    report_if = classification_report(y_true, y_pred_if, output_dict=True)
    report_svm = classification_report(y_true, y_pred_svm, output_dict=True)
    report_rf = classification_report(y_true, y_pred_rf, output_dict=True)

    # Convert results to CSV
    csv_buffer = StringIO()
    new_data.to_csv(csv_buffer, index=False)

    # Upload results to S3
    s3.put_object(Bucket=bucket_name, Key=results_file_path, Body=csv_buffer.getvalue())

    return {
        'statusCode': 200,
        'body': json.dumps({
            'report_if': report_if,
            'report_svm': report_svm,
            'report_rf': report_rf,
        })
    }
