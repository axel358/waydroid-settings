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
SYSTEM_IMAGE = ''
BASE_PROP_LOC = '/var/lib/waydroid/waydroid_base.prop'
ROOT_PW = ''

# System.img paths
SYSTEM_IMAGE1 = '/var/lib/waydroid/images/system.img'
SYSTEM_IMAGE2 = '/usr/share/waydroid-extra/images/system.img'

# Check whether the specified path exists
# Depending on install type, this might change 
if os.path.exists(SYSTEM_IMAGE1):
    SYSTEM_IMAGE = SYSTEM_IMAGE1
elif os.path.exists(SYSTEM_IMAGE2):
    SYSTEM_IMAGE = SYSTEM_IMAGE2

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
            subprocess.run('echo "' + ROOT_PW + '" | sudo -S ' + command, shell=True)
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


def is_kb_disabled():
    try:
        kb_val = subprocess.check_output('echo "' + ROOT_PW + '" | echo "pm list packages -d 2>/dev/null | grep com.android.inputmethod.latin | wc -l" | sudo -S waydroid shell', shell=True)
        print("kb_val: " + str(kb_val))
        return '1' in str(kb_val)
    except subprocess.CalledProcessError:
        return False


def is_correct_pass(password):
    try:
        subprocess.check_output('echo "' + password + '" | sudo -S echo 1', shell=True)
        return True
    except subprocess.CalledProcessError:
        return False


def set_prop(name, value):
    return run('waydroid prop set ' + name + ' ' + value, True)


def run_shell_command(command):
    return subprocess.run('echo "' + ROOT_PW + '" | echo "' + command + '" | sudo -S waydroid shell', shell=True, text=True)


def is_waydroid_running():
    try:
        waydroid_status = subprocess.check_output(['waydroid', 'status']).strip().decode("utf-8")
        return 'RUNNING' in waydroid_status
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def is_container_active():
    try:
        container_status = subprocess.check_output(
            ['systemctl', 'is-active', 'waydroid-container.service']).strip().decode("utf-8")
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
        return str('{:.3f}'.format(os.path.getsize(SYSTEM_IMAGE) / (1024 * 1024 * 1024))) + ' GB'
    except FileNotFoundError:
        return 0


def resize_image(new_size):
    run('systemctl stop waydroid-container.service', True)
    run('resize2fs ' + SYSTEM_IMAGE + ' ' + new_size + 'G', True)
    run('e2fsck -f ' + SYSTEM_IMAGE, True)
    start_container_service()
    start_session()


def wipe_data():
    run('systemctl stop waydroid-container.service', True)
    run('rm -rf ' + str(Path.home()) + '/.local/share/waydroid/data', True)
    run('waydroid init -f', True)
    start_container_service()
    start_session()


def search_base_prop(prop):
    try:
        prop_file = open(BASE_PROP_LOC, "r")
        for line in prop_file:
            if prop in line:
                return True
    except FileNotFoundError:
        return False

    return False


def enable_navbar():
    try:
        print('enabling navbar')
        run('sed -i "/qemu.hw.mainkeys=1/d" ' + BASE_PROP_LOC)
        restart_session()
        return True
    except:
        return False


def disable_navbar():
    try:
        print('disabling navbar')
        run('echo "qemu.hw.mainkeys=1" >> ' + BASE_PROP_LOC)
        restart_session()
        return True
    except:
        return False


def enable_kb():
    try:
        print('enabling keyboard')
        run_shell_command("pm enable com.android.inputmethod.latin")
        return True
    except:
        return False


def disable_kb():
    try:
        print('disabling keyboard')
        run_shell_command("pm disable com.android.inputmethod.latin")
        return True
    except:
        return False
    
def install_apk(apk):
    run('waydroid app install', True)
