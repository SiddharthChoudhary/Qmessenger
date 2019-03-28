# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loginserver.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from threading import Thread,Event
import EncryptorData
import select
import socket, sys, pickle
server = None
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', 3490))
        server.listen(5)
        self.encryptordata  = EncryptorData.EncryptorData()
        self.encryptordata.loginServer=server
        print("loginServer is ",server)
        self.encryptordata.loginServerInputs.extend([self.encryptordata.loginServer])
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(245, 41, 271, 491))
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(130, 10, 521, 16))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "This is a login server window. Here you can see the number of users who are online"))

class LoginServerThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.listofUsers = []
        self.encryptordata  = EncryptorData.EncryptorData()
        self.inputs = []
        self.outputs=[]
        self.exceptions=[]
        self.running=True
        self.switch = Event()
        self.switch.clear()
    def run(self):
        while self.switch.is_set:
            inputready,outputready,exceptready = select.select(self.encryptordata.loginServerInputs, self.encryptordata.loginServerOutputs,self.encryptordata.loginServerInputs,1)
            for s in inputready:
                if s is self.encryptordata.loginServer:
                    client, address = self.encryptordata.loginServer.accept()
                    self.encryptordata.loginServerInputs.extend([client])
                    print("client's getpeername is ", client.getpeername(), " and the list now is", self.listofUsers)
                    self.listofUsers.extend([client.getpeername()])
                    self.sendingObject = pickle.dumps(self.listofUsers)
                    print("sendingObject is ",self.sendingObject)
                    for o in self.encryptordata.loginServerOutputs:
                        o.send(self.sendingObject)
                    client.setblocking(0)
                    self.encryptordata.loginServerOutputs.extend([client])
                else:
                    try:
                        data = s.recv(1024)
                        message = data.decode('utf-8')
                        if 'socketOff:' in message:
                            mes,sockname = message.split(':') 
                            for s in self.encryptordata.loginServerInputs:
                                if sockname is s.getpeername():
                                    self.encryptordata.loginServerInputs.remove(s)
                                    self.encryptordata.loginServerOutputs.remove(s)
                                    self.listofUsers.remove(sockname)
                            for o in self.encryptordata.loginServerOutputs:
                                self.sendingObject = pickle.dumps(self.listofUsers)
                                o.send(self.sendingObject)
                        pass
                    except Exception as e:
                        self.encryptordata.loginServerInputs.remove(s)
                        self.encryptordata.loginServerOutputs.remove(s)
            for s in exceptready:
                self.encryptordata.inputs.remove(s)
                if s in self.encryptordata.outputs:
                    self.encryptordata.outputs.remove(s)
                s.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    loginServer = LoginServerThread()
    loginServer.start()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
