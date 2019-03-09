# -*- coding:utf-8 -*-
'''
Created on 2019年3月3日

@author: bkd
'''

import os

from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog,QFileDialog
from kdLaunchPad.fileutil import get_file_realpath

class sessionItem(QDialog):
    def __init__(self,last_path = None):
        super().__init__()
        loadUi("sessionItem.ui", self)
        self.last_path = last_path
    
    @pyqtSlot()
    def on_pb_open_file_clicked(self):
        filename, _ = QFileDialog.getOpenFileName(self,
                                    "选择文件",
                                     self.last_path,
                                    "All Files (*)")   #设置文件扩展名过滤,注意用双分号间隔
        if filename:
            print(filename)
            self.le_cmd.setText(filename)
            self.le_name.setText(os.path.basename(filename))
