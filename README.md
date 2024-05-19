## Generate Training and Testing Data

```shell
# Training Data
python network_traffic_generator.py --output_file data/training_network_traffic_data.csv --output_labels_file data/training_labels.csv --num_normal_logs 100000 --num_abnormal_logs 10000 --num_high_frequency_logs 5000

# Testing Data
python network_traffic_generator.py --output_file data/testing_network_traffic_data.csv --output_labels_file data/testing_labels.csv --num_normal_logs 2000 --num_abnormal_logs 200 --num_high_frequency_logs 50
```

## Data Preprocessing

```shell
python local/preprocessing.py --input_file data/training_network_traffic_data.csv --output_file_data data/preprocessed_data.csv --output_file_labels data/labels.csv --output_columns_file model/columns.pkl --imputer_file model/imputer.pkl --scaler_file model/scaler.pkl
```

## Model Training

```shell
python local/model_training.py --data_file data/preprocessed_data.csv --labels_file data/training_labels.csv --iso_forest_file model/iso_forest_model.pkl --svm_file model/svm_model.pkl --rf_file model/rf_model.pkl
```

## Verify the anomaly detection with testing data

```shell
python local/anomaly_detection.py --new_data_file data/testing_network_traffic_data.csv --output_file data/anomaly_detection_results.csv --iso_forest_file model/iso_forest_model.pkl --svm_file model/svm_model.pkl --rf_file model/rf_model.pkl --labels_file data/testing_labels.csv --columns_file model/columns.pkl --imputer_file model/imputer.pkl --scaler_file model/scaler.pkl
```
