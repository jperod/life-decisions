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

class GitUtils:

    @staticmethod
    def add_commit_push(file_path:str) -> None:
        print(f"Adding {file_path} to git remote")
        run_command(f"git add {file_path}")
        run_command("git pull origin")
        try:
            run_command('git commit -m "Auto Update README.md with latest information"')
            run_command("git push origin main")
        except:
            print("No changes to commit.")
