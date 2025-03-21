import os
import time

def monitor_events():
    print("Starting event monitoring...")
   
    while True:
        
        event = {"time": time.ctime(), "type": "file_access", "details": "/etc/passwd"}
        print(f"Event: {event}")
        time.sleep(2) 

if __name__ == "__main__":
    monitor_events()
