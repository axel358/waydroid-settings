#!/usr/bin/env python3

import sys
import os
import utils
import glob
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QObject, Qt, Property
from PySide2.QtGui import QStandardItem, QStandardItemModel


class MainWindow(QObject):

    SCRIPT_NAME_ROLE = Qt.UserRole
    SCRIPT_PATH_ROLE = Qt.UserRole + 1

    def __init__(self):
        QObject.__init__(self)
        self._scripts_model = QStandardItemModel()
        self._scripts_model.setItemRoleNames(
            {self.SCRIPT_NAME_ROLE: b"name", self.SCRIPT_PATH_ROLE: b"path"})

        self.update_scripts_list()

    def get_scripts_model(self):
        return self._scripts_model

    scripts_model = Property(QObject, fget=get_scripts_model, constant=True)

    def load_values(self):

        self._refreshing = True

        self.free_form_switch.set_active(
            utils.search_base_prop('persist.waydroid.multi_windows=true'))
        self.color_invert_switch.set_active(
            utils.get_prop(utils.PROP_INVERT_COLORS) == 'true')
        self.suspend_switch.set_active(utils.get_prop(
            utils.PROP_SUSPEND_INACTIVE) == 'true')
        self.nav_btns_switch.set_active(
            utils.search_base_prop('qemu.hw.mainkeys=1'))
        self.soft_kb_switch.set_active(utils.is_kb_disabled())

        if not utils.is_container_active():
            # Start Container Service
            pass

        if not utils.is_waydroid_running():
            # Start Session
            pass
        else:
            # Show Session options
            pass

        self._refreshing = False

    def update_scripts_list(self):

        self._scripts_model.clear()

        script_list = glob.glob(utils.SCRIPTS_DIR+'/**/*.sh',
                                recursive=True) + \
            glob.glob(utils.SCRIPTS_DIR+'/**/*.py', recursive=True)

        for script in script_list:
            item = QStandardItem()
            item.setData(os.path.basename(script), self.SCRIPT_NAME_ROLE)
            item.setData(script, self.SCRIPT_PATH_ROLE)
            self._scripts_model.appendRow(item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('Waydroid Settings')
    engine = QQmlApplicationEngine()
    main = MainWindow()

    engine.rootContext().setContextProperty('backend', main)
    engine.load('ui/main.qml')

    sys.exit(app.exec_())
