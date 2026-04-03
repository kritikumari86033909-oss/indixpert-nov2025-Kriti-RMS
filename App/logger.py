import os
from datetime import datetime

class Logger:

    def __init__(self):
        base_dir = os.getcwd()  
        self.log_dir = os.path.join(base_dir, "App", "logs")

        os.makedirs(self.log_dir, exist_ok=True)

        self.activity_log = os.path.join(self.log_dir, "activity.log")
        self.error_log = os.path.join(self.log_dir, "error.log")

    def log_activity(self, action, message):
        try:
            with open(self.activity_log, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] ACTION: {action} | {message}\n")
        except PermissionError:
            print(" Log file locked (close file and retry)")

    def log_error(self, error_msg):
        try:
            with open(self.error_log, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] ERROR: {error_msg}\n")
        except PermissionError:
            print(" Error log file locked")