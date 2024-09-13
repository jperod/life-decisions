import subprocess
import datetime
import pytz

def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode == 0:
        print(result.stdout)
    else:
        raise SystemError(f"Error: {result.stderr}")
    
def get_now_cph():
    return datetime.datetime.now().astimezone(pytz.timezone("Europe/Copenhagen"))

def get_now_cph_str():
    return get_now_cph().strftime("%Y-%m-%d %H:%M")