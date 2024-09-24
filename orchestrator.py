import schedule
import time
import subprocess
import datetime
import os
import sys
import pytz

now_cph = {datetime.datetime.now().astimezone(pytz.timezone("Europe/Copenhagen")).strftime("%Y-%m-%d %H:%M")}

def calculate_jacket_decision():
    print(f"Executing job `calculate_jacket_decision` at {now_cph}")
    venv_python_path = os.path.join(os.path.dirname(sys.executable), 'python')
    script_path = r"C:\Repos\life-decisions\jacket\exec_jacket_decision.py"
    subprocess.run([venv_python_path, script_path])

schedule.every(5).minutes.do(calculate_jacket_decision)

calculate_jacket_decision()
while True: 
    schedule.run_pending()
    time.sleep(1)  # Sleep for 1 sec to prevent high CPU usage