## Deployment Steps

### Preprocessing Lambda Function:
* Build and push the Docker image to ECR.
* Deploy the Lambda function using the image.

### Model Training with SageMaker:
* Use the SageMaker notebook to train the models and save them to S3.

### Anomaly Detection Lambda Function:
* Build and push the Docker image to ECR.
* Deploy the Lambda function using the image.