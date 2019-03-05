# -*- coding:utf-8 -*-
'''
Created on 2019年3月3日

@author: bkd
'''

import os

from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog,QFileDialog

class sessionItem(QDialog):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(os.getcwd(),"sessionItem.ui"), self)
        print("sessionItem init")
#         self.show()
    
    @pyqtSlot()
    def on_pb_open_file_clicked(self):
        filename, _ = QFileDialog.getOpenFileName(self,
                                    "选择文件",
                                    os.path.expanduser('~') ,
                                    "All Files (*)")   #设置文件扩展名过滤,注意用双分号间隔
        if filename:
            print(filename)
            self.le_cmd.setText(filename)
            self.le_name.setText(os.path.basename(filename))
#     @pyqtSlot()
#     def on_buttonBox_accepted(self):
#         session_item = {}
#         session_item["name"] = self.le_name.text()
#         session_item["cmd"] = self.le_cmd.text()
#         self.session_item = session_item
#         print(self.session_item)
#         return session_item
