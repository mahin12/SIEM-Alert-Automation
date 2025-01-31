# Alert Management and Automation System

## **Overview**
This project showcases an automated security operations system designed for detecting, processing, and responding to alerts. It integrates **Splunk** for alert generation, **Python** for scripting and automation, and **Jira** for ticket management. Additionally, it provides a **real-time dashboard** for visualizing alerts and incident data.

---

## **Key Features**
1. **Alert Processing**:
   - Parses alerts from Splunk logs for brute force, failed logins, phishing attempts, and port scans.
   - Filters and prioritizes high-severity alerts.

2. **Automation with Jira**:
   - Automatically creates and updates tickets in Jira for high-priority incidents.

3. **Real-Time Visualization**:
   - Displays high-priority tickets and alert summaries using a dynamic dashboard built with HTML and Chart.js.

4. **Reporting**:
   - Generates summary reports for frequent alert types and targeted IPs.

---

## **Technologies Used**
- **Splunk**: Ingestion and processing of security logs.
- **Python**: Scripting for automation and integration.
- **Jira API**: Automated ticket creation and updates.
- **Chart.js**: Data visualization for the dashboard.
- **HTML/CSS**: Dashboard frontend.
- **JSON**: Data storage and API responses.

---

## **Setup and Installation**

### **Prerequisites**
1. Python 3.x installed.
2. Access to Splunk and Jira APIs.
3. Flask framework for running the web application.
4. A web server (e.g., Nginx, Apache) for hosting the dashboard.

### **Installation Steps**
1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Required Python Packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up API Credentials**:
   - Update `splunk_to_jira.py` with your Splunk and Jira API keys and endpoints.

4. **Run the Flask App**:
   ```bash
   python app.py
   ```

5. **Access the Dashboard**:
   - Open `http://127.0.0.1:5001` in your browser.

---

## **Usage**

### **1. Monitoring Alerts**
- Splunk processes logs and generates alerts.
- Alerts are sent to the Flask application for further processing.

### **2. Incident Response**
- High-severity alerts are automatically converted into Jira tickets.
- Tickets contain details such as alert type, IP address, and timestamps.

### **3. Visualization**
- Access the dashboard to view:
  - High-priority tickets.
  - Alert trends and targeted IPs through bar and pie charts.

---

## **Code Breakdown**

### **1. Splunk-to-Jira Integration (`splunk_to_jira.py`)**
- Automates the creation of Jira tickets based on Splunk alerts.
- Example Code:
   ```python
   @app.route("/splunk-webhook", methods=["POST"])
   def splunk_webhook():
       splunk_data = request.json
       jira_payload = {
           "fields": {
               "project": {"key": JIRA_PROJECT_KEY},
               "summary": f"High-Severity Alert: {splunk_data['type']}",
               "description": f"Details:\nType: {splunk_data['type']}\nIP: {splunk_data['ip']}",
               "issuetype": {"name": "Task"}
           }
       }
       headers = {"Authorization": JIRA_AUTH, "Content-Type": "application/json"}
       response = requests.post(JIRA_URL, headers=headers, json=jira_payload)
       return {"status": response.status_code, "response": response.text}
   ```

### **2. Alert Processing (`alert_processing.py`)**
- Processes and filters alerts based on severity.
- Example Code:
   ```python
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
   ```

### **3. Dashboard (`index.html`)**
- Displays:
  - High-priority tickets.
  - Bar and pie charts for alert types and targeted IPs.
- Built with **Chart.js** and fetches data dynamically from APIs.

---

## **Example Outputs**

### **1. Splunk Dashboard**
![Splunk Dashboard Example](file:///mnt/data/Screenshot%202025-01-26%20at%207.58.57%E2%80%AFPM.png)

### **2. Jira Tickets**
![Jira Tickets](file:///mnt/data/Screenshot%202025-01-26%20at%208.03.25%E2%80%AFPM.png)

### **3. HTML Dashboard**
![HTML Dashboard](file:///mnt/data/Screenshot%202025-01-26%20at%208.02.13%E2%80%AFPM.png)

---

## **Future Enhancements**
1. Integrate machine learning models for advanced threat detection.
2. Expand the system to support additional SIEM tools.
3. Enhance the dashboard with role-based access control and granular filtering options.

---

## **Contributors**
- **Mahin Arafat**

---

## **License**
This project is licensed under the MIT License. See the LICENSE file for more information.







## generate JIRA

curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"type": "Brute Force Attack", "ip": "192.168.1.50", "message": "Multiple failed login attempts detected"}' \
    http://127.0.0.1:5001/splunk-webhook

curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"type": "Failed Login", "ip": "192.168.1.206", "message": "High-severity failed login attempts detected", "timestamp": "2025-01-26T22:40:28"}' \
    http://127.0.0.1:5001/splunk-webhook

curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"type": "Port Scan", "ip": "192.168.1.111", "message": "Medium-severity port scan activity detected", "timestamp": "2025-01-26T23:24:28"}' \
    http://127.0.0.1:5001/splunk-webhook

curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"type": "Phishing Attempt", "ip": "192.168.1.238", "message": "Medium-severity phishing attempt detected", "timestamp": "2025-01-26T22:35:28"}' \
    http://127.0.0.1:5001/splunk-webhook


## generate Random Alert

http://127.0.0.1:5000/send_alerts_to_splunk

## Splunk links

https://prd-p-jpzww.splunkcloud.com/en-GB/app/search/fd_project

index="test_alerts" sourcetype="fake_alerts" | table _time, type, severity, ip	

## Jira

https://mahinarafatmeem.atlassian.net/jira/software/projects/SCRUM/boards/1