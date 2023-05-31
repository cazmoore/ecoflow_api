import config
import csv
import notifications
import os
import requests

ECOFLOW_ENDPOINT = config.ECOFLOW_ENDPOINT
ECOFLOW_APPKEY = config.ECOFLOW_APPKEY
ECOFLOW_SECRETKEY = config.ECOFLOW_SECRETKEY

headers = {
    "appKey": ECOFLOW_APPKEY,
    "secretKey": ECOFLOW_SECRETKEY
}

upper_charge_threshold = 80
lower_charge_threshold = 20

# cwd = os.getcwd()


def check_device_status(key, value):
    data_file = f"{value} data.csv"
    params = {
        "sn": key
    }

    prev_soc = None

    response = requests.get(ECOFLOW_ENDPOINT, params=params, headers=headers)
    response.raise_for_status()
    message = response.json()["message"]

    if message == "Success":
        data = response.json()["data"]
        soc = int(data["soc"])
        time_remaining_mins = data["remainTime"]
        watts_out = data["wattsOutSum"]
        watts_in = data["wattsInSum"]
        # print(soc, time_remaining_mins, watts_out, watts_in)

        file_header = ["Serial #", "Device name", "SOC", "Time remaining (mins)", "Watts out", "Watts in"]
        data = [key, value, soc, time_remaining_mins, watts_in, watts_out]

        try:
            with open(data_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == key:
                        prev_soc = int(row[2])
                    else:
                        continue
        except FileNotFoundError:
            pass

        if prev_soc is None:
            pass
        elif prev_soc <= (upper_charge_threshold - 1) and soc >= upper_charge_threshold:
            title = f"{value} is now charged to {upper_charge_threshold}%."
            message = f"{value} is now charged to {upper_charge_threshold}%. Stop charging."
            notifications.send_push_notification(message, title)
        elif prev_soc >= (lower_charge_threshold + 1) and soc <= lower_charge_threshold:
            title = f"{value} is below {lower_charge_threshold}%."
            message = f"{value} is below {lower_charge_threshold}%. Recharge now."
            notifications.send_push_notification(message, title)
        elif prev_soc < 100 and soc == 100:
            title = f"{value} is fully charged."
            message = f"{value} is fully charged. Stop charging."
            notifications.send_push_notification(message, title)

        with open(data_file, "w", encoding="UTF8") as f:
            writer = csv.writer(f)

            writer.writerow(file_header)
            writer.writerow(data)
