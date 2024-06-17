# Authenticate Docker to your ECR registry
aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 869472115623.dkr.ecr.ap-southeast-1.amazonaws.com

# Data Ingrestion
docker build --platform linux/amd64 -t data-ingestion -f Dockerfile.data_ingestion .
docker tag data-ingestion:latest 869472115623.dkr.ecr.ap-southeast-1.amazonaws.com/data-ingestion:latest
docker push 869472115623.dkr.ecr.ap-southeast-1.amazonaws.com/data-ingestion:latest

# Data preprocessing
docker build --platform linux/amd64 -t preprocessing -f Dockerfile.preprocessing .
docker tag preprocessing:latest 869472115623.dkr.ecr.ap-southeast-1.amazonaws.com/preprocessing:latest
docker push 869472115623.dkr.ecr.ap-southeast-1.amazonaws.com/preprocessing:latest

# Data preprocessing
docker build --platform linux/amd64 -t preprocessing -f Dockerfile.preprocessing .
docker tag preprocessing:latest 869472115623.dkr.ecr.ap-southeast-1.amazonaws.com/preprocessing:latest
docker push 869472115623.dkr.ecr.ap-southeast-1.amazonaws.com/preprocessing:latest

# SageMaker Training
docker build --platform linux/amd64 -t sagemaker-training -f Dockerfile.sagemaker_training .
docker tag sagemaker-training:latest 869472115623.dkr.ecr.ap-southeast-1.amazonaws.com/sagemaker-training:latest
docker push 869472115623.dkr.ecr.ap-southeast-1.amazonaws.com/sagemaker-training:latest
