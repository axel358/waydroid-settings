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
SYSTEM_IMAGE = '/var/lib/waydroid/images/system.img'

# Scripts Paths 
scripts_dir1 = str(Path.home()) + '/.local/share/waydroid-settings/scripts/'
scripts_dir2 = '/usr/share/waydroid-settings/scripts/'

# Check whether the specified path exists
# Depending on install type, this might change 
if os.path.isdir(scripts_dir1):
    SCRIPTS_DIR = scripts_dir1
elif os.path.isdir(scripts_dir2):
    SCRIPTS_DIR = scripts_dir2
    
def run(command, as_root=False):
    try:
        if as_root:
            subprocess.run('pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY sudo ' + command, shell=True)
        else:
            subprocess.run(command, shell=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_prop(name):
    try:
        return subprocess.check_output(['waydroid', 'prop', 'get', name]).strip().decode("utf-8")
    except (subprocess.CalledProcessError, FileNotFoundError):
        return 'get_prop_error'


def set_prop(name, value):
    return run('waydroid prop set ' + name + ' ' + value, True)

def is_waydroid_running():
    try:
        waydroid_status = subprocess.check_output(['waydroid', 'status']).strip().decode("utf-8")
        return 'RUNNING' in waydroid_status
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def is_container_active():
    try:
        container_status = subprocess.check_output(['systemctl', 'is-active', 'waydroid-container.service']).strip().decode("utf-8")
        return 'active' in container_status
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def start_container_service():
    return run('systemctl restart waydroid-container.service', True)
        
def freeze_container():
    return run('waydroid container freeze', True)

def unfreeze_container():
    return run('waydroid container unfreeze &', True)

def start_session():
    return run('waydroid session start &')

def stop_session():
    return run('waydroid session stop &')

def restart_session():
    print("restarting container service")
    start_container_service()
    print("restarting session")
    start_session()
    
def get_image_size():
    try:
        return os.path.getsize(SYSTEM_IMAGE)
    except FileNotFoundError:
        return 0
        
def resize_image(new_size):
    run('resize2fs '+ new_size + 'G ' + SYSTEM_IMAGE, True)
    
def wipe_data():
    run('rm -r ' + str(Path.home()) + '/.local/share/waydroid/data')
    run('waydroid init -f', True)
    
