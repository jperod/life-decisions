import schedule
import time
import subprocess
import datetime
import os
import sys

def job():
    venv_python_path = os.path.join(os.path.dirname(sys.executable), 'python')
    script_path = r"C:\Repos\life-decisions\jacket\jacket.py"
    subprocess.run([venv_python_path, script_path])

# Schedule the job every 20 minutes
schedule.every(60).minutes.do(job)

while True:
    print(datetime.datetime.now())
    schedule.run_pending()
    time.sleep(60)  # Sleep for 60 seconds to prevent high CPU usage