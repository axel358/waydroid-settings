import subprocess
import os
from pathlib import Path


class Utils():

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
    SCRIPTS_DIR = '/home/axel/.local/share/waydroid-settings/scripts/'
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

    # Always prefer user scripts dir
    # Depending on install type, this might change

    if os.path.isdir(
            dir2 := '/home/axel/.local/share/waydroid-settings/scripts/'):
        SCRIPTS_DIR = dir2

    def run(self, command, as_root=False):
        try:
            if as_root:
                subprocess.run('pkexec waydroid-helper ' + '"' + command + '"',
                               shell=True)
            else:
                subprocess.run(command, shell=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def get_prop(self, name):
        try:
            return subprocess.check_output(['waydroid', 'prop', 'get',
                                            name]).strip().decode("utf-8")
        except (subprocess.CalledProcessError, FileNotFoundError):
            return 'get_prop_error'

    def is_kb_disabled(self):
        return False
        try:
            kb_val = subprocess.check_output(
                'echo "' + ROOT_PW +
                '" | echo "pm list packages -d 2>/dev/null | grep com.android.inputmethod.latin | wc -l" | sudo -S waydroid shell',
                shell=True)
            return '1' in str(kb_val)
        except subprocess.CalledProcessError:
            return False

    def set_prop(self, name, value):
        return self.run('waydroid prop set ' + name + ' ' + value, True)

    def run_shell_command(self, command):
        return subprocess.run('echo "' + ROOT_PW + '" | echo "' + command +
                              '" | sudo -S waydroid shell',
                              shell=True,
                              text=True)

    def is_waydroid_running(self):
        try:
            waydroid_status = subprocess.check_output(
                ['waydroid', 'status']).strip().decode("utf-8")
            return 'RUNNING' in waydroid_status
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def is_container_active(self):
        try:
            container_status = subprocess.check_output(
                ['systemctl', 'is-active',
                 'waydroid-container.service']).strip().decode("utf-8")
            return 'active' in container_status
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def start_container_service(self):
        return self.run('systemctl restart waydroid-container.service', True)

    def freeze_container(self):
        return self.run('waydroid container freeze', True)

    def unfreeze_container(self):
        return self.run('waydroid container unfreeze &', True)

    def start_session(self):
        return self.run('waydroid session start &')

    def stop_session(self):
        return self.run('waydroid session stop &')

    def restart_session(self):
        self.start_container_service()
        self.start_session()

    def get_image_size(self):
        try:
            return str('{:.3f}'.format(
                os.path.getsize(self.SYSTEM_IMAGE) /
                (1024 * 1024 * 1024))) + ' GB'
        except FileNotFoundError:
            return 0

    def resize_image(self, new_size):
        self.run('systemctl stop waydroid-container.service', True)
        self.run('resize2fs ' + SYSTEM_IMAGE + ' ' + new_size + 'G', True)
        self.run('e2fsck -f ' + SYSTEM_IMAGE, True)
        self.start_container_service()
        self.start_session()

    def wipe_data(self):
        self.run('systemctl stop waydroid-container.service', True)
        self.run('rm -rf ' + str(Path.home()) + '/.local/share/waydroid/data',
                 True)
        self.run('waydroid init -f', True)
        self.start_container_service()
        self.start_session()

    def search_base_prop(self, prop):
        try:
            prop_file = open(self.BASE_PROP_LOC, "r")
            for line in prop_file:
                if prop in line:
                    return True
        except FileNotFoundError:
            return False

        return False

    def enable_navbar(self):
        try:
            self.run('sed -i "/qemu.hw.mainkeys=1/d" ' + BASE_PROP_LOC)
            self.restart_session()
            return True
        except BaseException:
            return False

    def disable_navbar(self):
        try:
            self.run('echo "qemu.hw.mainkeys=1" >> ' + BASE_PROP_LOC)
            self.restart_session()
            return True
        except BaseException:
            return False

    def disable_freeform_override(self):
        try:
            self.run('sed -i "/persist.waydroid.multi_windows=true/d" ' +
                     BASE_PROP_LOC)
            self.restart_session()
            return True
        except BaseException:
            return False

    def enable_freeform_override(self):
        try:
            self.run('echo "persist.waydroid.multi_windows=true" >> ' +
                     BASE_PROP_LOC)
            self.restart_session()
            return True
        except BaseException:
            return False

    def enable_kb(self):
        try:
            self.run_shell_command("pm enable com.android.inputmethod.latin")
            return True
        except BaseException:
            return False

    def disable_kb(self):
        try:
            run_shell_command("pm disable com.android.inputmethod.latin")
            return True
        except BaseException:
            return False

    def install_apk(self, apk):
        self.run('waydroid app install ' + apk, True)
