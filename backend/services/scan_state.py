import os
import json

STATE_FILE = "scan_state.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return {}

    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def get_folder_modified_time(path):
    return os.path.getmtime(path)