from datetime import datetime
import os

# cwd = os.getcwd()
log_file = "run_log.txt"
now = datetime.now()
now = now.strftime("%A, %d %B, %Y at %-I:%M%p")


def log_script_run():
    with open(log_file, "w", encoding="UTF8") as f:
        f.write(f"Script last successfully run at: {now}.")
