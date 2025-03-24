import os
import time
import sqlite3
import yaml
from analyzer import analyze_events

# [Previous functions: setup_database, log_event, load_config unchanged]

def monitor_events():
    setup_database()
    config = load_config()
    monitored_types = config["monitored_events"]
    print("Starting event monitoring...")
    while True:
        event = {"time": time.ctime(), "type": "file_access", "details": "/etc/passwd"}
        if event["type"] in monitored_types:
            log_event(event)
            print(f"Logged: {event}")
        analyze_events()  # Check for anomalies
        time.sleep(2)

if __name__ == "__main__":
    monitor_events()
