# sagemaker_training_job.py
import boto3

sagemaker = boto3.client('sagemaker')

response = sagemaker.create_training_job(
    TrainingJobName='network-anomaly-detection-training',
    AlgorithmSpecification={
        'TrainingImage': '869472115623.dkr.ecr.ap-southeast-1.amazonaws.com/sagemaker-training:latest',
        'TrainingInputMode': 'File'
    },
    RoleArn='sagemaker-execution-role',
    InputDataConfig=[
        {
            'ChannelName': 'training',
            'DataSource': {
                'S3DataSource': {
                    'S3DataType': 'S3Prefix',
                    'S3Uri': 's3://bkimp-ads/data/',
                    'S3DataDistributionType': 'FullyReplicated'
                }
            },
            'ContentType': 'text/csv',
            'InputMode': 'File'
        }
    ],
    OutputDataConfig={
        'S3OutputPath': 's3://bkimp-ads/model/'
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
