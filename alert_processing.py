from flask import Flask, jsonify, render_template
import json
from collections import defaultdict
import random
from datetime import datetime, timedelta
import requests

# Generate random alerts
def generate_random_alerts(count=10):
    alert_types = ["Brute Force", "Failed Login", "Port Scan", "Phishing Attempt"]
    severities = ["low", "medium", "high"]
    alerts = []

    for i in range(1, count + 1):
        alerts.append({
            "id": i,
            "type": random.choice(alert_types),
            "severity": random.choice(severities),
            "ip": f"192.168.1.{random.randint(1, 255)}",
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 60))).strftime("%Y-%m-%dT%H:%M:%S")
        })

    return alerts

# Splunk HEC details
SPLUNK_URL = "" #Splunk HEC endpoint
SPLUNK_TOKEN = ""  # Splunk HEC token

#token


# Send alerts to Splunk
def send_to_splunk(alerts):
    headers = {"Authorization": f"Splunk {SPLUNK_TOKEN}"}
    for alert in alerts:
        payload = {
            "event": alert,
            "sourcetype": "fake_alerts",
            "index": "test_alerts"
        }
        try:
            response = requests.post(SPLUNK_URL, headers=headers, json=payload, verify=False)  # Disable SSL verification
            if response.status_code == 200:
                print(f"Successfully sent alert: {alert}")
            else:
                print(f"Failed to send alert: {alert}. Response: {response.text}")
        except Exception as e:
            print(f"Error sending alert to Splunk: {e}")


# Process alerts
def process_alerts(alerts):
    high_priority_tickets = []
    summary = {"alert_type_count": defaultdict(int), "ip_count": defaultdict(int)}

    for alert in alerts:
        if alert["severity"] == "high":
            high_priority_tickets.append({
                "ticket_id": f"T-{alert['id']}",
                "description": f"Investigate {alert['type']} from {alert['ip']}",
                "timestamp": alert["timestamp"],
            })

        summary["alert_type_count"][alert["type"]] += 1
        if "ip" in alert:
            summary["ip_count"][alert["ip"]] += 1

    return high_priority_tickets, summary

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_alerts_to_splunk")
def send_alerts_to_splunk():
    alerts = generate_random_alerts(10)
    send_to_splunk(alerts)
    return jsonify({"status": "Alerts sent to Splunk", "alerts": alerts})

@app.route("/tickets")
def get_tickets():
    alerts = generate_random_alerts(10)  # Generate fake alerts for testing
    tickets, _ = process_alerts(alerts)
    return jsonify(tickets)

@app.route("/summary")
def get_summary():
    alerts = generate_random_alerts(10)  # Generate fake alerts for testing
    _, summary = process_alerts(alerts)
    summary["alert_type_count"] = dict(summary["alert_type_count"])
    summary["ip_count"] = dict(summary["ip_count"])
    return jsonify(summary)

if __name__ == "__main__":
    app.run(debug=True)



