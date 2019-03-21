# -*- coding:utf-8 -*-
'''
Created on 2019年3月3日

@author: bkd
'''

import sys
import os

from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot,Qt,QPoint,pyqtSignal
from PyQt5.QtWidgets import QWidget,QListView,QSizePolicy,QAction,QMenu,QInputDialog,QLineEdit
from PyQt5.QtGui import QStandardItem,QStandardItemModel,QCursor
from .sessionItem import sessionItem
from .fileutil import get_file_realpath


class launchSession(QWidget):
    add_item_signal = pyqtSignal(dict)
    del_item_signal = pyqtSignal(dict)
    alter_session_signal = pyqtSignal(str,str)
    del_session_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        loadUi(get_file_realpath("launchSession.ui"), self)
        self.maxSize = QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum)
        
        self.popMenu = QMenu()
        self.bold = [QAction("新增"),QAction("删除")]
        self.lv_session.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lv_session.customContextMenuRequested[QPoint].connect(self.myListWidgetContext)

        self.lb_session_pop_menu = QMenu()
        self.lb_session_pop_menu_item = [QAction("修改会话"),QAction("删除会话")]
        self.lb_session_name.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lb_session_name.customContextMenuRequested[QPoint].connect(self.handle_lb_session_name_pop_menu)
        
        self.model = QStandardItemModel()
        self.lv_session.setSizePolicy(self.maxSize)
        self.lv_session.setModel(self.model)
        self.lv_session.setViewMode(QListView.ListMode)
        self.lv_session.doubleClicked.connect(self.on_item_doubleClicked)
        
        self.last_path = os.path.expanduser('~')

    def init_session(self,conf):
        session_name = conf["session_name"]
        self.session_name = session_name
        session_list = conf["session_list"]
        self.lb_session_name.setText(session_name)
        self.lv_session.setObjectName(session_name)
        print("add new session," + session_name)

        if session_list:
            for session_list_item in session_list:
                standard_item = QStandardItem(session_list_item["name"])
                standard_item.setData(session_list_item["cmd"])
                standard_item.setEditable(False)
                self.model.appendRow(standard_item)
#                 self.lv_session.addItem(session_list_item["name"])
    @pyqtSlot()
    def on_item_doubleClicked(self):
        cur_index = self.lv_session.currentIndex()
        cmd = self.model.item(cur_index.row(), 0).data()
        print(cmd)
        self.run_cmd(cmd)
    @pyqtSlot()
    def on_pb_launch_clicked(self):
        print("get",self.model.rowCount())
        for i in range(self.model.rowCount()):
            cmd = self.model.item(i).data()
            print(self.model.item(i).data())
            self.run_cmd(cmd)
        sys.exit(0)
        
    def run_cmd(self,cmd):
        if os.name == "nt":
            os.startfile(cmd)
        elif os.name == "posix":
            os.system(cmd + " &")
        print(os.name)
    def myListWidgetContext(self):
        action = self.popMenu.exec_(self.bold,QCursor.pos())
        if action:
            action_text = action.text()
            print(action_text)
            if action_text == "新增" :
                self.s = sessionItem(self.last_path)
                if self.s.exec_():
                    print(self.s.le_name.text())
                    standard_item = QStandardItem(self.s.le_name.text())
                    standard_item.setData(self.s.le_cmd.text())
                    standard_item.setEditable(False)
                    self.model.appendRow(standard_item)
#                     self.model.insertRow(self.model.rowCount(),standard_item)
#                     standard_item.setEnabled(True)
#                     self.lv_session.setVisible(True)
                    
                    session_item = {"name":self.s.le_name.text(),"cmd":self.s.le_cmd.text(),"session_name":self.session_name}
                    self.last_path = self.s.le_cmd.text()
                    self.add_item_signal.emit(session_item)
            elif action_text == "删除" :
                cur_index = self.lv_session.currentIndex()
                name = self.model.item(cur_index.row(), 0).text() 
                print(name)
                session_item = {"name":name,"session_name":self.session_name}
                self.del_item_signal.emit(session_item)
                self.model.removeRow(cur_index.row())
#                 s.show()
            
    def handle_lb_session_name_pop_menu(self):
        action = self.lb_session_pop_menu.exec_(self.lb_session_pop_menu_item,QCursor.pos())
        if action:
            action_text = action.text()
            if action_text == "修改会话" :
                new_session_name, ok = QInputDialog.getText(self, "会话标题", "请输入会话标题:", QLineEdit.Normal)
                if ok:
                    self.lb_session_name.setText(new_session_name)
                    self.alter_session_signal.emit(self.session_name,new_session_name)
            elif action_text == "删除会话":
                self.del_session_signal.emit(self.session_name)
                self.close()
