# -*- coding:utf-8 -*-
'''
Created on 2019年3月3日

@author: bkd
'''

from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import sys
import os

from PyQt5.QtCore import pyqtSlot,Qt,QPoint,pyqtSignal
from PyQt5.QtWidgets import QWidget,QListView,QSizePolicy,QAction,QMenu,QInputDialog,QLineEdit
from PyQt5.QtGui import QStandardItem,QStandardItemModel,QCursor
from sessionItem import sessionItem


class launchSession(QWidget):
    add_item_signal = pyqtSignal(dict)
    del_item_signal = pyqtSignal(dict)
    alter_session_signal = pyqtSignal(str,str)
    del_session_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        loadUi(sys.path[0] +"/launchSession.ui", self)
        self.maxSize = QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum)
        
        self.popMenu = QMenu()
        self.bold = [QAction("新增"),QAction("删除")]
        self.lv_session.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lv_session.customContextMenuRequested[QPoint].connect(self.myListWidgetContext)

        self.lb_session_pop_menu = QMenu()
        self.lb_session_pop_menu_item = [QAction("修改会话"),QAction("删除会话")]
        self.lb_session_name.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lb_session_name.customContextMenuRequested[QPoint].connect(self.handle_lb_session_name_pop_menu)
        

    def init_session(self,conf):
        session_name = conf["session_name"]
        self.session_name = session_name
        session_list = conf["session_list"]
        self.lb_session_name.setText(session_name)
        self.lv_session.setObjectName(session_name)
        self.lv_session.setSizePolicy(self.maxSize)
        print("add new session," + session_name)

        self.model = QStandardItemModel()
        if session_list:
            for session_list_item in session_list:
                standard_item = QStandardItem(session_list_item["name"])
                standard_item.setData(session_list_item["cmd"])
                self.model.appendRow(standard_item)
#                 self.lv_session.addItem(session_list_item["name"])
            self.lv_session.setModel(self.model)
            self.lv_session.setViewMode(QListView.ListMode)
            self.lv_session.clicked.connect(self.on_item_changed)
            self.lv_session.setSizePolicy(self.maxSize)
    @pyqtSlot()
    def on_item_changed(self):
        cur_index = self.lv_session.currentIndex()
        print(self.model.item(cur_index.row(), 0).data())
#         print(dir(qModelIndex))
#         print(qModelIndex.row())
    @pyqtSlot()
    def on_pb_launch_clicked(self):
        print("get",self.model.rowCount())
        for i in range(self.model.rowCount()):
            cmd = self.model.item(i).data()
            print(self.model.item(i).data())
            os.system(cmd + " &")
        
    def myListWidgetContext(self):
        action = self.popMenu.exec_(self.bold,QCursor.pos())
        if action:
            action_text = action.text()
            print(action_text)
            if action_text == "新增" :
                self.s = sessionItem()
                if self.s.exec_():
                    print(self.s.le_name.text())
                    standard_item = QStandardItem(self.s.le_name.text())
                    standard_item.setData(self.s.le_cmd.text())
                    self.model.appendRow(standard_item)
                    
                    session_item = {"name":self.s.le_name.text(),"cmd":self.s.le_cmd.text(),"session_name":self.session_name}
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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = launchSession()
    win.show()
    sys.exit(app.exec_())
