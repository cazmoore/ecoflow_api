import config
import notifications
import os

SERVER_IP = config.SERVER_IP
STATUS_FILE = "ping_status.txt"


def check_host_status():
    previous_status = read_previous_status()

    current_status = {}
    status_changed = False

    for key, value in SERVER_IP.items():
        response = os.system('ping -c 1 ' + key)
        if response == 0:
            current_status[key] = "UP"
            status_message = f"{value} status has changed. Server is now {current_status[key]}."
        else:
            current_status[key] = "DOWN"
            status_message = f"{value} status has changed. Server is now {current_status[key]}. Possible power outage."

        if current_status[key] != previous_status.get(key):
            status_changed = True

        write_status_to_file(current_status)

        if status_changed:
            title = "Host status changed"
            message = status_message
            notifications.send_push_notification(message, title)


def read_previous_status():
    previous_status = {}
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as file:
            for line in file:
                key, value = line.strip().split(':')
                previous_status[key] = value
    return previous_status


def write_status_to_file(status):
    with open(STATUS_FILE, 'w') as file:
        for key, value in status.items():
            file.write(f"{key}:{value}\n")


check_host_status()

