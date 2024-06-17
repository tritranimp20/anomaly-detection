# Model Training in local
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.svm import OneClassSVM
import pandas as pd
import joblib
import os
import argparse

def train_models(data_file, labels_file, iso_forest_file, svm_file, rf_file):
    # Ensure the 'model' directory exists
    os.makedirs('model', exist_ok=True)

    # Load preprocessed data
    X = pd.read_csv(data_file)
    y = pd.read_csv(labels_file)

    # Train Isolation Forest
    iso_forest = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
    iso_forest.fit(X)

    # Train One-Class SVM
    svm = OneClassSVM(kernel='rbf', gamma=0.1, nu=0.01)
    svm.fit(X)

    # Train Random Forest Classifier
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y.values.ravel())

    # Save models to local storage in the 'model' folder
    joblib.dump(iso_forest, iso_forest_file)
    joblib.dump(svm, svm_file)
    joblib.dump(rf, rf_file)

    print(f"Models saved to {os.path.abspath('model')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train machine learning models.')
    parser.add_argument('--data_file', type=str, default='data/preprocessed_data.csv', help='Input CSV file with preprocessed data')
    parser.add_argument('--labels_file', type=str, default='data/labels.csv', help='Input CSV file with labels')
    parser.add_argument('--iso_forest_file', type=str, default='model/iso_forest_model.pkl', help='Output file for Isolation Forest model')
    parser.add_argument('--svm_file', type=str, default='model/svm_model.pkl', help='Output file for One-Class SVM model')
    parser.add_argument('--rf_file', type=str, default='model/rf_model.pkl', help='Output file for Random Forest model')
    args = parser.parse_args()

    train_models(args.data_file, args.labels_file, args.iso_forest_file, args.svm_file, args.rf_file)
