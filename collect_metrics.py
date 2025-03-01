import psutil
import pandas as pd
import time
from datetime import datetime

LOG_FILE = "server_usage.csv"

def log_usage():
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent

        data = pd.DataFrame([[timestamp, cpu_usage, memory_usage]],
                            columns=["timestamp", "cpu_usage", "memory_usage"])

        data.to_csv(LOG_FILE, mode="a", header=not pd.io.common.file_exists(LOG_FILE), index=False)

        time.sleep(59)  # Log every minute

if __name__ == "__main__":
    log_usage()