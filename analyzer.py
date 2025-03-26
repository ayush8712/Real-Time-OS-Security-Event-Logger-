import sqlite3
from collections import Counter
import time
import json
from datetime import datetime

# Define known attack patterns (simplified for demo)
KNOWN_PATTERNS = {
    "brute_force": {"type": "login_attempt", "threshold": 5, "time_window": 300},  # 5 attempts in 5 mins
    "privilege_escalation": {"type": "sudo_command", "details_contains": "root"}
}

# Severity scoring rules (customizable)
SEVERITY_RULES = {
    "file_access": {"base_score": 2, "critical_path": ["/etc/passwd", "/etc/shadow"], "critical_bonus": 5},
    "login_attempt": {"base_score": 3, "failed_bonus": 2},
    "sudo_command": {"base_score": 5, "root_bonus": 3}
}

def analyze_events():
    """Analyze recent events for anomalies, severity, and patterns."""
    conn = sqlite3.connect("security_events.db")
    c = conn.cursor()
    # Fetch events from the last 5 minutes
    c.execute("SELECT time, type, details FROM events WHERE time > datetime('now', '-5 minutes')")
    recent_events = c.fetchall()
    conn.close()

    if not recent_events:
        return {"message": "No recent events to analyze"}

    # 1. Frequency-based anomaly detection
    event_counts = Counter((e[1], e[2]) for e in recent_events)  # (type, details)
    anomalies = []
    for (event_type, details), count in event_counts.items():
        if count > 3:  # Threshold for anomaly
            anomalies.append(f"High frequency: {count} {event_type} events for {details}")

    # 2. Severity scoring
    severity_scores = []
    for event_time, event_type, details in recent_events:
        score = calculate_severity(event_type, details)
        severity_scores.append({"time": event_time, "type": event_type, "details": details, "severity": score})

    # 3. Pattern matching
    patterns_detected = match_patterns(recent_events)

    # 4. Compile results
    analysis_result = {
        "timestamp": datetime.now().isoformat(),
        "anomalies": anomalies,
        "severity_scores": sorted(severity_scores, key=lambda x: x["severity"], reverse=True)[:5],  # Top 5 by severity
        "patterns_detected": patterns_detected
    }

    # 5. Log results to file
    log_analysis_results(analysis_result)

    # Print summary for console
    print(f"Analysis at {analysis_result['timestamp']}:")
    if anomalies:
        print("Anomalies:", "; ".join(anomalies))
    if patterns_detected:
        print("Patterns:", "; ".join(patterns_detected))
    print(f"Top severity event: {analysis_result['severity_scores'][0] if analysis_result['severity_scores'] else 'None'}")

    return analysis_result

def calculate_severity(event_type, details):
    """Assign a severity score based on event type and details."""
    rules = SEVERITY_RULES.get(event_type, {"base_score": 1})
    score = rules["base_score"]

    # Apply additional rules
    if event_type == "file_access" and "critical_path" in rules:
        if any(path in details for path in rules["critical_path"]):
            score += rules["critical_bonus"]
    elif event_type == "login_attempt" and "failed" in details.lower():
        score += rules["failed_bonus"]
    elif event_type == "sudo_command" and "root" in details.lower():
        score += rules["root_bonus"]

    return score

def match_patterns(events):
    """Check events against known attack patterns."""
    detected = []
    event_counts = Counter((e[1], e[2]) for e in events)  # (type, details)

    for pattern_name, pattern in KNOWN_PATTERNS.items():
        if pattern_name == "brute_force":
            for (event_type, details), count in event_counts.items():
                if event_type == pattern["type"] and count >= pattern["threshold"]:
                    detected.append(f"Brute force detected: {count} {event_type} attempts")
        elif pattern_name == "privilege_escalation":
            for _, event_type, details in events:
                if event_type == pattern["type"] and pattern["details_contains"] in details.lower():
                    detected.append(f"Privilege escalation detected: {event_type} with {details}")

    return detected

def log_analysis_results(result):
    """Save analysis results to a JSON file."""
    with open("analysis_log.json", "a") as f:
        json.dump(result, f)
        f.write("\n")  # Newline for readability

if __name__ == "__main__":
    # Test the analyzer standalone
    analyze_events()
