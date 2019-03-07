# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loginserver.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from threading import Thread
import select
import socket, sys
server = None
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
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
    def __init__(self,ui):
        Thread.__init__(self)
        self.ui=ui
        self.listofUsers = []
        self.running=True
    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(0)
        server.bind(('localhost', 3490))
        server.listen(5)
        inputs =[server,sys.stdin]
        outputs= []
        while self.running:
            try:
                    inputready,outputready,exceptready = select.select(inputs, outputs, inputs,1)
            except Exception as e:
                print("Got exception",e)
                break
            except Exception as e:
                    print("Got exception", e)
                    break
            for s in inputready:
                if s is server:
                    print("I am runing")
                    client, address = server.accept()
                    inputs.extend([client])
                    for o in outputs:
                        send(o,self.listofUsers)
                    client.setblocking(0)
                    outputs.append([client])
                    pass

                elif s is sys.stdin:
                    msg = sys.stdin.readline()
                    if msg is "exit":
                        for o in outputs:
                            send(o,"LoginServer Going down")
                        server.close()
                        exit()
                else:
                    try:
                        pass
                    except Exception as e:
                        inputs.remove(s)
                        self.outputs.remove(s)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    loginServer = LoginServerThread(ui)
    loginServer.start()
    MainWindow.show()
    sys.exit(app.exec_())
