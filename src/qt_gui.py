#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： 11360
# datetime： 2021/5/17 22:30 
# import pyqt5
import PyQt5
from PyQt5 import QtGui, QtCore, QtWidgets
import qdarkstyle
import sys
import threading
import os
import socket
from widget_control_tello import TelloControllerWidget
from tello import Tello


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.showMaximized()
        self.setWindowTitle("Tello Scan")
        self.tello_obj = Tello('', 8889)
        self.control_widget = TelloControllerWidget(self.tello_obj, self)
        self.set_layout()

    def set_layout(self):
        hlayout = QtWidgets.QHBoxLayout(self)
        hlayout.addWidget(self.control_widget)
        self.setLayout(hlayout)

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               '',
                                               "Are you sure to Exit？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            # self.control_widget.thread_get_video.join()
            # self.control_widget.thread_send_command.join()
            self.control_widget.stop_event.set()
            del self.tello_obj
            # self.close()
            self.deleteLater()
            os._exit(0)
            # del self.control_widget.thread_send_command
            # sys.exit()
        else:
            event.ignore()

class PathPlanningWidget(QtWidgets.QWidget):
    def __init__(self):
        super(PathPlanningWidget, self).__init__()


class SavephotosWidget(QtWidgets.QWidget):
    def __init__(self):
        super(SavephotosWidget, self).__init__()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    myshow = MainWindow()  # 主窗口实例化
    sys.exit(app.exec_())


