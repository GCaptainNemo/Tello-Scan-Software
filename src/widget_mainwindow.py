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
from widget_path_planning import PathPlanningWidget
from tello import Tello
from utils import *
import numpy as np


class ThreadFollowPath(QtCore.QThread):
    def __init__(self, vec_lst, tello_obj):
        super(ThreadFollowPath, self).__init__()
        self.vec_lst = vec_lst
        self.tello_obj = tello_obj

    def run(self):
        print("in")
        for vec in self.vec_lst:
            index = np.argmax(np.abs(vec))
            if index == 0:
                if vec[index] >= 0:
                    self.tello_obj.move_forward(vec[index])
                else:
                    self.tello_obj.move_backward(-vec[index])
            elif index == 1:
                if vec[index] >= 0:
                    self.tello_obj.move_left(vec[index])
                else:
                    self.tello_obj.move_right(-vec[index])
            elif index == 2:
                if vec[index] >= 0:
                    self.tello_obj.move_forward(vec[index])
                else:
                    self.tello_obj.move_backward(-vec[index])
            self.sleep(5)
        self.deleteLater()


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Tello Scan")
        self.tello_obj = Tello('', 8889)
        self.control_widget = TelloControllerWidget(self.tello_obj)
        self.path_widget = PathPlanningWidget()
        self.path_widget.signal_trajectory_point.connect(self.start_trajectory)
        self.set_layout()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def start_trajectory(self, pos_lst):
        vec_lst = [(pos_lst[i+1] - pos_lst[i]) / 100 for i in range(len(pos_lst) - 1)]
        self.thread_follow_path = ThreadFollowPath(vec_lst, self.tello_obj)
        self.thread_follow_path.start()

    def set_layout(self):
        self.hsplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.hsplitter.addWidget(self.path_widget)
        self.hsplitter.addWidget(self.control_widget)
        hlayout = QtWidgets.QHBoxLayout(self)
        # hlayout.addWidget(self.control_widget)
        hlayout.addWidget(self.hsplitter)
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
            stop_thread(self.control_widget.thread_deal_video)
            stop_thread(self.control_widget.thread_send_command)
            stop_thread(self.tello_obj.receive_command_func)
            stop_thread(self.tello_obj.receive_video_thread)
            self.control_widget.stop_event.set()
            del self.tello_obj
            self.deleteLater()
        else:
            event.ignore()


class SavephotosWidget(QtWidgets.QWidget):
    def __init__(self):
        super(SavephotosWidget, self).__init__()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    myshow = MainWindow()  # 主窗口实例化
    myshow.showMaximized()
    sys.exit(app.exec_())



