#  OilGasSafety

> A web-based safety monitoring and analysis system for the Oil & Gas industry.  
> Built using Python (Backend) and HTML / CSS / JavaScript (Frontend).

## 📖 About

OilGasSafety is a simple safety-focused web application to monitor, analyze, and manage safety-related information in the oil and gas industry.  
It combines a Python backend server with a lightweight interactive frontend UI.

##  Screenshots

![image alt](https://github.com/chaitanya-suddamalla/OilGasSafety/blob/0b1f57d5ffb7cb4fcfafe76dddc5dde514ff0fb1/Screenshot%202026-01-07%20151122.png)
![image alt](https://github.com/chaitanya-suddamalla/OilGasSafety/blob/0b1f57d5ffb7cb4fcfafe76dddc5dde514ff0fb1/Screenshot%202026-01-07%20151643.png)


## 📁 Project Structure

```
OilGasSafety/
├─ 
├─ run.py                   # Main application entry point
├─ server.py                # Backend server logic
├─ requirements.txt         # Python dependencies
├─ start.bat                # Windows startup script
├─ .env                     # Environment variables (optional)
├─ .gitignore               # Git ignore rules
│
├─ index.html               # Frontend UI
├─ style.css                # UI styling
├─ script.js                # Client-side logic
│
├─ SETUP_INSTRUCTIONS.md    # Setup documentation
├─ QUICK_START.txt          # Quick start guide
├─ ARCHITECTURE.txt         # Architecture details
├─ COMMANDS.txt             # Useful commands
|
└─ PROJECT_COMPLETION.txt   # Final notes
 ```
 

## ✨ Features

- Python backend server
- Interactive web interface
- Modular project structure
- Easy local setup
- Windows startup support

## 🧰 Tech Stack

**Backend:** Python 3.x  
**Frontend:** HTML, CSS, JavaScript  
**Tools:** Git, GitHub

## 🚀 Installation & Usage

1. Clone the repository:
```
git clone https://github.com/chaitanya-suddamalla/OilGasSafety.git
cd OilGasSafety

```

### Run backend

-   `pip install -r requirements.txt`
-   `python run.py`

> Note: Python must be installed in the system (v3.9+ preferred). Configure env variables in the `.env` file.

Add these environment variables - GAS_SENSOR_API_KEY, SAFETY_ALERT_API, INCIDENT_REPORT_API


### configure .env file

You will need API keys for gas monitoring, safety alerts, and incident reporting services

1. Register with the gas monitoring or safety service provider used in the project

2. Generate an API key for gas sensor data and add it to the
   GAS_SENSOR_API_KEY env variable

3. Generate a safety alert API key and update the
   SAFETY_ALERT_API env variable

4. Generate an incident reporting API key and update the
   INCIDENT_REPORT_API env variable

You can visit the application at http://localhost:5000 in development mode.

  
