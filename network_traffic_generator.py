# network_traffic_generator.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
import argparse

# Function to generate random IP addresses
def generate_random_ip():
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

# Generate normal access logs
def generate_normal_logs(num_logs):
    logs = []
    base_time = datetime.now()
    for _ in range(num_logs):
        log = {
            'timestamp': base_time - timedelta(seconds=random.randint(0, 3600)),
            'src_addr': generate_random_ip(),
            'dst_addr': generate_random_ip(),
            'protocol': random.choice(['TCP', 'UDP']),  # Keep protocol as string
            'src_port': random.choice([80, 443, 22, 21, 25, 53]),  # Common service ports
            'dst_port': random.choice([80, 443, 22, 21, 25, 53]),
            'bytes': random.randint(500, 5000),  # Smaller, consistent data volume
            'cpu_usage': random.uniform(0, 50),  # Low to moderate CPU usage
            'memory_usage': random.uniform(0, 50),  # Low to moderate memory usage
            'disk_io': random.randint(100, 500),  # Low to moderate disk I/O
            'network_io': random.randint(100, 500),  # Low to moderate network I/O
            'action': 'ACCEPT',  # Generally accepted traffic
            'log_status': 'OK'
        }
        logs.append(log)
    return logs

# Generate abnormal access logs
def generate_abnormal_logs(num_logs):
    logs = []
    base_time = datetime.now()
    for _ in range(num_logs):
        log = {
            'timestamp': base_time - timedelta(seconds=random.randint(0, 3600)),
            'src_addr': generate_random_ip(),
            'dst_addr': generate_random_ip(),
            'protocol': random.choice(['TCP', 'UDP']),  # Keep protocol as string
            'src_port': random.randint(1024, 65535),  # Wide range of ports, including unusual ones
            'dst_port': random.randint(1, 1023),  # Might target unusual ports
            'bytes': random.randint(5000, 100000),  # Larger, variable data volume
            'cpu_usage': random.uniform(50, 100),  # High CPU usage
            'memory_usage': random.uniform(50, 100),  # High memory usage
            'disk_io': random.randint(500, 5000),  # High disk I/O
            'network_io': random.randint(500, 5000),  # High network I/O
            'action': random.choice(['REJECT', 'ACCEPT']),  # Mix of accepted and rejected traffic
            'log_status': 'OK'
        }
        logs.append(log)
    return logs

# Generate high frequency logs
def generate_high_frequency_logs(num_logs):
    logs = []
    base_time = datetime.now()
    for _ in range(num_logs):
        log = {
            'timestamp': base_time - timedelta(seconds=random.randint(0, 600)),  # Shorter time intervals
            'src_addr': generate_random_ip(),
            'dst_addr': generate_random_ip(),
            'protocol': random.choice(['TCP', 'UDP']),  # Keep protocol as string
            'src_port': random.randint(1024, 65535),
            'dst_port': random.randint(1, 1023),
            'bytes': random.randint(5000, 100000),
            'cpu_usage': random.uniform(50, 100),
            'memory_usage': random.uniform(50, 100),
            'disk_io': random.randint(500, 5000),
            'network_io': random.randint(500, 5000),
            'action': random.choice(['REJECT', 'ACCEPT']),
            'log_status': 'OK'
        }
        logs.append(log)
    return logs

def generate_data(output_file, output_labels_file, num_normal_logs, num_abnormal_logs, num_high_frequency_logs):
    # Generate dataset
    normal_logs = generate_normal_logs(num_normal_logs)
    abnormal_logs = generate_abnormal_logs(num_abnormal_logs)
    high_frequency_logs = generate_high_frequency_logs(num_high_frequency_logs)

    # Combine and label the logs
    all_logs = normal_logs + abnormal_logs + high_frequency_logs
    for log in all_logs:
        if log in normal_logs:
            log['label'] = 0  # Normal
        elif log in abnormal_logs:
            log['label'] = 1  # Anomaly
        else:
            log['label'] = 2  # High frequency anomaly

    # Convert to DataFrame
    df = pd.DataFrame(all_logs)

    # Save the dataset to CSV
    df.to_csv(output_file, index=False)
    df[['label']].to_csv(output_labels_file, index=False)

    # Display a sample of the dataset
    print(df.head())
    print(f"Synthetic data generation completed. Data saved to {output_file} and labels saved to {output_labels_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate synthetic network traffic data.')
    parser.add_argument('--output_file', type=str, default='data/network_traffic_data.csv', help='Output CSV file for synthetic data')
    parser.add_argument('--output_labels_file', type=str, default='data/network_traffic_labels.csv', help='Output CSV file for labels')
    parser.add_argument('--num_normal_logs', type=int, default=1000, help='Number of normal logs to generate')
    parser.add_argument('--num_abnormal_logs', type=int, default=100, help='Number of abnormal logs to generate')
    parser.add_argument('--num_high_frequency_logs', type=int, default=50, help='Number of high frequency logs to generate')
    args = parser.parse_args()

    generate_data(args.output_file, args.output_labels_file, args.num_normal_logs, args.num_abnormal_logs, args.num_high_frequency_logs)
