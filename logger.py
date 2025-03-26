import time
import sqlite3
import yaml
from analyzer import analyze_events
import random

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
    event_types = ["file_access", "login_attempt", "sudo_command"]
    details_options = {
        "file_access": ["/etc/passwd", "/home/user.txt"],
        "login_attempt": ["Failed login from 192.168.1.10", "Success login"],
        "sudo_command": ["sudo -u root", "sudo ls"]
    }
    print("Starting event monitoring...")
    while True:
        event_type = random.choice(event_types)
        event = {
            "time": time.ctime(),
            "type": event_type,
            "details": random.choice(details_options[event_type])
        }
        if event["type"] in monitored_types:
            log_event(event)
            print(f"Logged: {event}")
        analyze_events()  # Run enhanced analysis
        time.sleep(1)  # Faster for testing

if _name_ == "_main_":
    monitor_events()
