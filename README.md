# Real-Time OS Security Event Logger

A Python-based tool to monitor, log, and analyze operating system security events in real time, providing insights into potential vulnerabilities. This project was developed with a modular design and includes event logging, analysis, and visualization features, demonstrated through 7+ GitHub revisions.

## Project Overview

The Real-Time OS Security Event Logger captures OS-level security events (simulated for this demo), stores them in a SQLite database, analyzes them for anomalies and patterns, and presents the results via a graphical user interface (GUI). It’s built to be extensible and user-friendly, making it a valuable tool for system administrators or security enthusiasts.

### Goals
- Monitor and log security events in real time.
- Detect anomalies and potential threats (e.g., brute force attacks).
- Visualize event trends for better decision-making.

### Scope
- Focuses on simulated events (e.g., file access, login attempts) for demonstration.
- Includes basic analysis and visualization; expandable to real OS event sources like `auditd`.

## Features

- **Event Logging:** Captures and stores events in a SQLite database with configurable filtering.
- **Event Analysis:** Detects anomalies (e.g., high-frequency events), assigns severity scores, and matches known attack patterns (e.g., brute force, privilege escalation).
- **Visualization:** Displays real-time logs and a bar graph of event frequency via a GUI.
- **Persistence:** Logs analysis results to a JSON file for auditing.

## Requirements

- Python 3.x
- Dependencies:
  - `pyyaml` (for config file parsing)
  - `matplotlib` (for graphing)
- Git (for cloning the repository)

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone <your-repo-url>
   cd os-security-logger

   ## Demo Website
View the project overview online: [Live Demo](https://yourusername.github.io/os-security-logger/)
