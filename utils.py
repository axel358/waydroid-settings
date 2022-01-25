import subprocess
import os
from pathlib import Path

PROP_FREE_FORM = 'persist.waydroid.multi_windows'
PROP_INVERT_COLORS = ''
PROP_SUSPEND_INACTIVE = 'persist.waydroid.suspend'
PROP_WINDOW_WIDTH = 'persist.waydroid.width'
PROP_WINDOW_HEIGHT = 'persist.waydroid.height'
PROP_WINDOW_WIDTH_PADDING = 'persist.waydroid.width_padding'
PROP_WINDOW_HEIGHT_PADDING = 'persist.waydroid.height_padding'
PROP_BLACKLISTED_APPS = 'waydroid.blacklist_apps'
PROP_ACTIVE_APPS = 'waydroid.active_apps'
DOCS_URL = 'https://docs.waydro.id/'
HOME_URL = 'https://waydro.id/'

# Scripts Paths 
scripts_dir1 = str(Path.home()) + '/.local/share/waydroid-settings/scripts/'
scripts_dir2 = '/usr/share/waydroid-settings/scripts/'

# Check whether the specified path exists
# Depending on install type, this might change 
if os.path.isdir(scripts_dir1):
    SCRIPTS_DIR = scripts_dir1
elif os.path.isdir(scripts_dir2):
    SCRIPTS_DIR = scripts_dir2 

def get_prop(name):
    try:
        return subprocess.check_output(['waydroid', 'prop', 'get', name]).strip().decode("utf-8")
    except (subprocess.CalledProcessError, FileNotFoundError):
        return 'get_prop_error'


def set_prop(name, value):
    try:
        print("Set Prop Running")
        subprocess.run('pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY waydroid prop set ' + name + ' ' + value, shell=True)
        return 'ok'
    except:
        return 'set_prop_error'

def is_waydroid_running():
    try:
        waydroid_status = subprocess.check_output(['waydroid', 'status']).strip().decode("utf-8")
        if 'STOPPED' in waydroid_status:
            return False
        elif 'RUNNING' in waydroid_status:
            return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

    return True

def get_waydroid_container_service():
    try:
        waydroid_container_service = subprocess.check_output(['systemctl', 'is-active', 'waydroid-container.service']).strip().decode("utf-8")
        print(len(waydroid_container_service))
        print("")
        print(waydroid_container_service)
        if 'inactive' in waydroid_container_service:
            return "container service stopped"
        else:
            return "running"        
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        waydroid_container_service = "Failed"
        return waydroid_container_service

def start_container_service():
    try:
        print("starting Container Service")
        subprocess.run('pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY sudo systemctl restart waydroid-container.service', shell=True)
        return 'ok'
    except:
        return 'service_error'

def start_session():
    try:
        print("starting session")
        os.system("waydroid session start &")
        return 'ok'
    except:
        return 'service_error'

def restart_session():
    try:
        print("restarting container service")
        start_container_service()
        print("restarting session")
        os.system("waydroid session start &")
        return 'ok'
    except:
        return 'service_error'
