"""
logger module

This module is used to write messages to the log.
"""

from datetime import datetime
import os

script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]
rel_path = "resources/log.txt"
log_path = os.path.join(script_dir, rel_path)

def log(message):
    """Adds a message to the end of the log"""
    time = datetime.now()
    time_string = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, 'a') as f:
        f.write("[" + time_string + "] " + message + "\n")

def clear():
    """Clears the log"""
    with open(log_path, 'w') as f:
        f.truncate()