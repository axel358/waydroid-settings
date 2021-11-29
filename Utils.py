import subprocess


def get_prop(name):
    try:
        return subprocess.check_output('waydroid prop get ' + name)
    except:
        return 'error'


def set_prop(name, value):
    try:
        subprocess.run('waydroid prop set ' + name + ' ' + value)
        return 'ok'
    except:
        return 'error'
