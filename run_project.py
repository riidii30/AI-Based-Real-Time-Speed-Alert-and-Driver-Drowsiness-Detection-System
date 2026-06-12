import subprocess
import time
import webbrowser

# LIVE SERVER FRONTEND URL

FRONTEND_URL = "http://127.0.0.1:5500/Frontend/index.html"

# BACKEND PATH

backend_path = "Backend"

# START FLASK BACKEND

print("Starting Flask Backend...")

backend_process = subprocess.Popen(

    ["python3", "app.py"],

    cwd=backend_path
)

# WAIT FOR BACKEND

time.sleep(3)

# START AI DROWSINESS DETECTION

print("Starting AI Drowsiness Detection...")

ai_process = subprocess.Popen(

    [

        "ai_env/bin/python3",

        "drowsiness.py"

    ],

    cwd=backend_path
)

# WAIT FOR CAMERA

time.sleep(2)

# OPEN FRONTEND

print("Opening Frontend...")

webbrowser.open(

    FRONTEND_URL
)

# PROJECT STATUS

print("\n✅ Smart Speed Alert System Running")

print("✅ Flask Backend Started")

print("✅ AI Drowsiness Detection Started")

print("✅ Frontend Opened")

print("✅ Open Dashboard Separately if Needed")

# KEEP PROJECT RUNNING

backend_process.wait()

ai_process.wait()