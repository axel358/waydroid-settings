#!/usr/bin/env python3

import sys
import os
import utils
import glob
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QObject, Qt, Property, Signal, Slot
from PySide2.QtGui import QStandardItem, QStandardItemModel


class MainWindow(QObject):

    SCRIPT_NAME_ROLE = Qt.UserRole
    SCRIPT_PATH_ROLE = Qt.UserRole + 1

    def __init__(self):
        QObject.__init__(self)
        self._scriptsModel = QStandardItemModel()
        self._scriptsModel.setItemRoleNames(
            {self.SCRIPT_NAME_ROLE: b"name", self.SCRIPT_PATH_ROLE: b"path"})

        self.updateScriptsList()

    def getScriptsModel(self):
        return self._scriptsModel

    scriptsModel = Property(QObject, fget=getScriptsModel, constant=True)

    freeFormChanged = Signal(bool)
    colorInvertChanged = Signal(bool)
    suspendChanged = Signal(bool)
    navButtonsChanged = Signal(bool)
    softKbChanged = Signal(bool)
    showToast = Signal(str)

    @Slot()
    def loadValues(self):

        self._refreshing = True

        self.freeFormChanged.emit(
            utils.search_base_prop('persist.waydroid.multi_windows=true'))
        self.colorInvertChanged.emit(
            utils.get_prop(utils.PROP_INVERT_COLORS) == 'true')
        self.suspendChanged.emit(utils.get_prop(
            utils.PROP_SUSPEND_INACTIVE) == 'true')
        self.navButtonsChanged.emit(
            utils.search_base_prop('qemu.hw.mainkeys=1'))
        self.softKbChanged.emit(utils.is_kb_disabled())

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

    def updateScriptsList(self):

        self._scriptsModel.clear()

        script_list = glob.glob(utils.SCRIPTS_DIR+'/**/*.sh',
                                recursive=True) + \
            glob.glob(utils.SCRIPTS_DIR+'/**/*.py', recursive=True)

        for script in script_list:
            item = QStandardItem()
            item.setData(os.path.basename(script), self.SCRIPT_NAME_ROLE)
            item.setData(script, self.SCRIPT_PATH_ROLE)
            self._scriptsModel.appendRow(item)

    @Slot(bool)
    def onFreeFormSwitchChanged(self, checked):
        pass

    @Slot(bool)
    def onColorInvertSwitchChanged(self, checked):
        pass

    @Slot(bool)
    def onSuspendSwitchChanged(self, checked):
        pass

    @Slot(bool)
    def onSoftKbSwitchChanged(self, checked):
        pass

    @Slot(bool)
    def onNavButtonsSwitchChanged(self, checked):
        pass

    @Slot(bool)
    def onFreezeSwitchChanged(self, checked):
        pass

    @Slot()
    def onRestartContainerClicked(self):
        pass

    @Slot()
    def onRestartSessionClicked(self):
        pass

    @Slot()
    def onStopSessionClicked(self):
        pass

    @Slot(str)
    def installApk(self, file):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('Waydroid Settings')
    engine = QQmlApplicationEngine()
    main = MainWindow()

    engine.rootContext().setContextProperty('backend', main)
    engine.load('ui/main.qml')

    sys.exit(app.exec_())
