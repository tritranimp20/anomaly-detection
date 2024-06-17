import boto3

sagemaker = boto3.client('sagemaker')

response = sagemaker.create_training_job(
    TrainingJobName='network-anomaly-detection-training',
    AlgorithmSpecification={
        'TrainingImage': 'your-training-image',
        'TrainingInputMode': 'File'
    },
    RoleArn='your-sagemaker-execution-role',
    InputDataConfig=[
        {
            'ChannelName': 'training',
            'DataSource': {
                'S3DataSource': {
                    'S3DataType': 'S3Prefix',
                    'S3Uri': 's3://your-processed-data-bucket/',
                    'S3DataDistributionType': 'FullyReplicated'
                }
            },
            'ContentType': 'text/csv',
            'InputMode': 'File'
        }
    ],
    OutputDataConfig={
        'S3OutputPath': 's3://your-model-bucket/'
    },
    ResourceConfig={
        'InstanceType': 'ml.m4.xlarge',
        'InstanceCount': 1,
        'VolumeSizeInGB': 10
    },
    StoppingCondition={
        'MaxRuntimeInSeconds': 3600
    }
)

print(response)
