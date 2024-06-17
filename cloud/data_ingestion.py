import boto3
import json
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta

def lambda_handler(event, context):
    logs_client = boto3.client('logs')
    s3 = boto3.client('s3')

    # Define CloudWatch Logs parameters
    log_group_name = '/aws/lambda/your-log-group'  # Replace with your log group name
    log_stream_name = 'your-log-stream'  # Replace with your log stream name
    start_time = int((datetime.utcnow() - timedelta(minutes=5)).timestamp() * 1000)  # Last 5 minutes
    end_time = int(datetime.utcnow().timestamp() * 1000)

    # Fetch logs from CloudWatch
    response = logs_client.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        startTime=start_time,
        endTime=end_time,
        limit=10000
    )

    # Process log events
    log_events = response['events']
    log_data = [json.loads(event['message']) for event in log_events]

    # Convert log data to DataFrame
    df = pd.DataFrame(log_data)

    # Convert DataFrame to CSV
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    # Define S3 bucket and file name
    bucket_name = 'bkimp-ads'
    file_path = 'data/raw/network_traffic_data.csv'

    # Upload CSV to S3
    s3.put_object(Bucket=bucket_name, Key=file_path, Body=csv_buffer.getvalue())

    return {
        'statusCode': 200,
        'body': json.dumps('Log data ingested and saved to S3 as CSV')
    }
