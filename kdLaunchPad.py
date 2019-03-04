#!/usr/bin/env python3
#-*- coding:utf-8 -*-
'''
Created on 2019年3月3日

@author: bkd
'''
from PyQt5.uic import loadUi
import os
import sys

from PyQt5.Qt import QMainWindow
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import  QApplication, QFileDialog,  QGraphicsOpacityEffect, QAction, QMenu, QInputDialog, QLineEdit

import kdconfigutil
from launchSession import launchSession


class kdLaunchPad(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi(sys.path[0] +"/kdLaunchPad.ui", self)
        self.setWindowIcon(QIcon(sys.path[0] +'/image/logo.ico'))
        
        self.confs = kdconfigutil.init_conf()
        print(self.confs)
        self.row = 0
        self.col = 0
        if self.confs:
            self.init_menu(self.confs)
        opacity_effect = QGraphicsOpacityEffect(self)
        opacity_effect.setOpacity(0.95)
        self.setGraphicsEffect(opacity_effect)
        
        self.pop_menu = QMenu()
        self.pop_menu_item = [QAction("新增会话"),QAction("设置背景")]
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested[QPoint].connect(self.handle_pop_menu)
        
        self.set_background_image(sys.path[0] +"/image/background.jpg")
        
    def init_menu(self,confs):
        for conf in confs:
            ls = launchSession()
            ls.init_session(conf)
            ls.add_item_signal.connect(self.add_session_item)
            ls.del_item_signal.connect(self.del_session_item)
            ls.alter_session_signal.connect(self.alter_session_name)
            ls.del_session_signal.connect(self.del_session)
            self.gridLayout.addWidget(ls,self.row,self.col)
            self.col += 1
            if self.col >= 3:
                self.col = 0
                self.row += 1
    def add_session_item(self,session_item):
        session_name = session_item["session_name"]
        for conf in self.confs:
            if conf["session_name"] == session_name :
                print(session_item)
                new_item = {"name":session_item["name"],"cmd":session_item["cmd"]}
                conf["session_list"].append(new_item)
                kdconfigutil.update_conf(self.confs)
                break
    def del_session_item(self,session_item):
        print("删除",session_item)
        session_name = session_item["session_name"]
        for conf in self.confs:
            if conf["session_name"] == session_name :
                for item in conf["session_list"]:
                    if item["name"] == session_item["name"] :
                        print(item["name"])
                        conf["session_list"].remove(item)
                        break
                kdconfigutil.update_conf(self.confs)
                break
        
    def handle_pop_menu(self):
        action = self.pop_menu.exec_(self.pop_menu_item,QCursor.pos())
        if action:
            action_text = action.text()
            if action_text == "新增会话" :
                value, ok = QInputDialog.getText(self, "会话标题", "请输入会话标题:", QLineEdit.Normal)
                if ok:
                    ls = launchSession()
                    ls.lb_session_name.setText(value)
                    ls.add_item_signal.connect(self.add_session_item)
                    ls.del_item_signal.connect(self.del_session_item)
                    self.gridLayout.addWidget(ls,self.row,self.col)
                    self.col += 1
                    if self.col >= 3:
                        self.col = 0
                        self.row += 1
                    new_session = {"session_name":value,"session_list":[]}
                    self.confs.append(new_session)
                    kdconfigutil.update_conf(self.confs)
                    self.repaint()
            elif action_text == "设置背景":
                filename, _ = QFileDialog.getOpenFileName(self,
                            "选择背景文件",
                            os.environ["HOME"],
                            "(*.jpg);;(*.png)")   #设置文件扩展名过滤,注意用双分号间隔
                if filename:
                    print(filename)
                    self.set_background_image(filename)
                
    def alter_session_name(self,old_session_name,new_session_name):
        for conf in self.confs:
            if conf["session_name"] == old_session_name:
                conf["session_name"] = new_session_name
                kdconfigutil.update_conf(self.confs)

    def del_session(self, old_session_name):
        print("删除" + old_session_name)
        for conf in self.confs:
            if conf["session_name"] == old_session_name:
                self.confs.remove(conf)
                print("删除会话成功" + old_session_name)
                kdconfigutil.update_conf(self.confs)
                self.col -= 1
                if self.col < 0 :
                    self.col = 2
                    self.row -= 1
                self.repaint()
               
    def set_background_image(self,filename):
        self.setStyleSheet("#MainWindow{border-image:url("+filename +");}")
        if filename != sys.path[0] +"/image/background.jpg":
            with open(filename,"rb") as new_background:
                with open(sys.path[0] +"/image/background.jpg","wb") as old_background:
                    old_background.write(new_background.read())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = kdLaunchPad()
    win.showFullScreen()
#     win.setWindowOpacity(0.9)
#     win.show()
    sys.exit(app.exec_())        