import os
import time
import sqlite3
import yaml

def setup_database():
    conn = sqlite3.connect("security_events.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events 
                 (id INTEGER PRIMARY KEY, time TEXT, type TEXT, details TEXT)''')
    conn.commit()
    conn.close()

def log_event(event):
    conn = sqlite3.connect("security_events.db")
    c = conn.cursor()
    c.execute("INSERT INTO events (time, type, details) VALUES (?, ?, ?)",
              (event["time"], event["type"], event["details"]))
    conn.commit()
    conn.close()

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

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
        time.sleep(2)

if __name__ == "__main__":
    monitor_events()
