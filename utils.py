import subprocess
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
SCRIPTS_DIR = str(Path.home()) + '/.local/share/waydroid-settings/scripts/'


def get_prop(name):
	try:
		return subprocess.check_output(['waydroid', 'prop', 'get', name]).strip().decode("utf-8")
	except (subprocess.CalledProcessError, FileNotFoundError):
		return 'get_prop_error'


def set_prop(name, value):
    try:
        subprocess.run('waydroid prop set ' + name + ' ' + value)
        return 'ok'
    except:
        return 'set_prop_error'