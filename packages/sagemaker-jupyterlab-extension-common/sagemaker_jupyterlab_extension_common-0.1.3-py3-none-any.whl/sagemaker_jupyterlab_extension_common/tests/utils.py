import os
import json
import tempfile
from pathlib import Path
import shutil

""""
This creates a temporary log file in the test folder, 
make sure to cleanup later by invoking the cleanup function and pass right path
"""

JUPTER_LOG_FILES_PATH = "jupterlab/"


def set_log_file_directory(env_var):
    log_path = Path(__file__).parents[1]
    os.environ[env_var] = str(log_path)
    log_path = os.path.join(log_path, JUPTER_LOG_FILES_PATH)
    return log_path


"""Read the last entry from the temporary logfile"""


def get_last_entry(file_name):
    # actual_path = os.environ.get(path_env).join(file_name)
    with open(file_name) as fid:
        lines = fid.readlines()
    return json.loads(lines[-1])


"""Remove the temporary logfile"""


def remove_temp_file_and_env(logile, env_var, filepath):
    os.remove(logile)
    os.rmdir(filepath)
    del os.environ[env_var]
