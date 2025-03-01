import psutil
import time
import csv
import os
from datetime import datetime, timedelta

# Configuration
LOG_FILE = "server_usage_log.csv"
INTERVAL = 5 * 60  # 5 minutes in seconds
RECORD_LIMIT = 24 * 60 * 60 // INTERVAL  # Number of records for 24 hours

def initialize_csv():
    """Create a CSV file with a header if it doesn't exist."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "cpu_percent", "memory_percent"])

def read_existing_records():
    """Read existing records from the CSV file."""
    records = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            records = list(reader)
    return records[-RECORD_LIMIT:]  # Keep only last 24 hours of records

def write_records(records):
    """Write records to the CSV file."""
    with open(LOG_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "cpu_percent", "memory_percent"])  # Write header
        writer.writerows(records)

def log_usage():
    """Log CPU and memory usage to CSV."""
    initialize_csv()
    records = read_existing_records()
    
    while True:
        usage_info = [
            datetime.now().isoformat(),
            psutil.cpu_percent(interval=1),
            psutil.virtual_memory().percent
        ]

        records.append(usage_info)
        records = records[-RECORD_LIMIT:]  # Keep only the last 24 hours of data
        write_records(records)

        time.sleep(INTERVAL - 1)  # Sleep for 5 minutes minus the interval used in `cpu_percent`

if __name__ == "__main__":
    log_usage()