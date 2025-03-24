import sqlite3
from collections import Counter

def analyze_events():
    conn = sqlite3.connect("security_events.db")
    c = conn.cursor()
    c.execute("SELECT type, details FROM events WHERE time > datetime('now', '-5 minutes')")
    recent_events = c.fetchall()
    conn.close()

  
    event_counts = Counter((e[0], e[1]) for e in recent_events)
    for (event_type, details), count in event_counts.items():
        if count > 3:  
            print(f"Anomaly detected: {count} {event_type} events for {details}")
