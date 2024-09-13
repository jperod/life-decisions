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
    def get_current_branch() -> str:
        """ Get the current Git branch name. """
        result = subprocess.run("git rev-parse --abbrev-ref HEAD", shell=True, text=True, capture_output=True)
        if result.returncode != 0:
            print("Error getting current branch.")
            return None
        return result.stdout.strip()

    @staticmethod
    def add_commit_push(file_path:str) -> None:
        current_branch = GitUtils.get_current_branch()
        print(f"Adding {file_path} to git remote on branch {current_branch}")
        if not current_branch:
            raise ValueError("Unable to determine the current Git branch.")
        run_command(f"git add {file_path}")

        run_command(f"git pull origin {current_branch}")
        try:
            run_command('git commit -m "Auto Update README.md with latest information"')
            run_command(f"git push origin {current_branch}")
        except:
            print("No changes to commit.")
