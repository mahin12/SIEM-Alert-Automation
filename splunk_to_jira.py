from flask import Flask, request
import requests
import json

app = Flask(__name__)

# JIRA API details
JIRA_URL = ""
JIRA_AUTH = ""
JIRA_PROJECT_KEY = ""

@app.route("/splunk-webhook", methods=["POST"])
def splunk_webhook():
    # Extract data from Splunk
    splunk_data = request.json

    # Transform Splunk data into JIRA payload
    jira_payload = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": f"High-Severity Alert: {splunk_data['type']}",
            "description": (
                f"Details:\n"
                f"Type: {splunk_data['type']}\n"
                f"IP: {splunk_data['ip']}\n"
                f"Message: {splunk_data.get('message', 'No message')}"
            ),
            "issuetype": {"name": "Task"}
        }
    }

    # Send data to JIRA
    headers = {
        "Authorization": JIRA_AUTH,
        "Content-Type": "application/json"
    }
    response = requests.post(JIRA_URL, headers=headers, json=jira_payload)

    # Return JIRA API response
    return {"status": response.status_code, "response": response.text}, response.status_code

if __name__ == "__main__":
    app.run(port=5001)
