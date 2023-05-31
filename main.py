import config
import ecoflow
import ping
import runlog

DEVICES = config.DEVICES

# Ping Raspberry Pi
ping.check_host_status()


# Check Ecoflow devices
def check_devices():
    for key, value in DEVICES.items():
        ecoflow.check_device_status(key, value)
    runlog.log_script_run()


check_devices()
