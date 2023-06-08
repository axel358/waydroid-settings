#!/usr/bin/env python3

import sys
import os
import KFPython
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QObject


class MainWindow(QObject):

    def __init__(self):
        QObject.__init__(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('Waydroid Settings')
    engine = QQmlApplicationEngine()
    main = MainWindow()

    engine.rootContext().setContextProperty('backend', main)
    engine.load('ui/main.qml')

    sys.exit(app.exec_())
