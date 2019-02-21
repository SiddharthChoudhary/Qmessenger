# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qc.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
from threading import Thread
import socket
import sys
import select
import signal
from threading import Thread
from communication import send, receive
ChatArea={}
server=None
dataTobeSent = None
class Ui_QMessenger(object):
    def setupUi(self, QMessenger,host='127.0.0.1',port=3490):
        QMessenger.setObjectName("QMessenger")
        QMessenger.resize(1280, 800)
        # Quit flag
        self.centralwidget = QtWidgets.QWidget(QMessenger)
        self.centralwidget.setObjectName("centralwidget")
        self.MessageArea = QtWidgets.QScrollArea(self.centralwidget)
        self.MessageArea.setGeometry(QtCore.QRect(20, 90, 381, 391))
        self.MessageArea.setWidgetResizable(True)
        self.MessageArea.setObjectName("MessageArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 379, 389))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ChatArea = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.ChatArea.setReadOnly(True)
        self.ChatArea.setObjectName("ChatArea")
        self.verticalLayout.addWidget(self.ChatArea)
        self.MessageArea.setWidget(self.scrollAreaWidgetContents)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 70, 60, 16))
        self.label_3.setObjectName("label_3")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(20, 510, 741, 51))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.ToSendText = QtWidgets.QPlainTextEdit(self.frame)
        self.ToSendText.setGeometry(QtCore.QRect(10, 10, 581, 31))
        self.ToSendText.setObjectName("ToSendText")
        self.SendButton = QtWidgets.QPushButton(self.frame)
        self.SendButton.setGeometry(QtCore.QRect(620, 10, 91, 31))
        self.SendButton.setObjectName("SendButton")
        self.SendButton.clicked.connect(self.sendData)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(420, 40, 401, 451))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame_2)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(29, 40, 161, 391))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.SendEncryptedMessagelistView = QtWidgets.QListView(self.verticalLayoutWidget)
        self.SendEncryptedMessagelistView.setObjectName("SendEncryptedMessagelistView")
        self.verticalLayout_2.addWidget(self.SendEncryptedMessagelistView)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.frame_2)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(220, 40, 160, 391))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.RecieveEncryptedMessageListview = QtWidgets.QListView(self.verticalLayoutWidget_2)
        self.RecieveEncryptedMessageListview.setObjectName("RecieveEncryptedMessageListview")
        self.verticalLayout_3.addWidget(self.RecieveEncryptedMessageListview)
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(210, 20, 181, 16))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setGeometry(QtCore.QRect(30, 20, 151, 16))
        self.label.setObjectName("label")
        self.onlineUsersArea = QtWidgets.QScrollArea(self.centralwidget)
        self.onlineUsersArea.setGeometry(QtCore.QRect(840, 30, 366, 611))
        self.onlineUsersArea.setWidgetResizable(True)
        self.onlineUsersArea.setObjectName("onlineUsersArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 364, 609))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 341, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.OnlineUser = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.OnlineUser.setAlignment(QtCore.Qt.AlignCenter)
        self.OnlineUser.setObjectName("OnlineUser")
        self.horizontalLayout.addWidget(self.OnlineUser)
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(30, 460, 301, 31))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.YourId = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        self.YourId.setObjectName("YourId")
        self.horizontalLayout_5.addWidget(self.YourId)
        self.onlineUsersArea.setWidget(self.scrollAreaWidgetContents_2)
        QMessenger.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(QMessenger)
        self.statusbar.setObjectName("statusbar")
        QMessenger.setStatusBar(self.statusbar)
        self.retranslateUi(QMessenger)
        QtCore.QMetaObject.connectSlotsByName(QMessenger)
    def retranslateUi(self, QMessenger):
        _translate = QtCore.QCoreApplication.translate
        QMessenger.setWindowTitle(_translate("QMessenger", "QMessenger"))
        self.label_3.setText(_translate("QMessenger", "Messages"))
        self.ToSendText.setToolTip(_translate("QMessenger", "<html><head/><body><p>Type your text here...</p></body></html>"))
        self.SendButton.setText(_translate("QMessenger", "Send"))
        self.label_2.setText(_translate("QMessenger", "Recieve Encrypted message"))
        self.label.setText(_translate("QMessenger", "Sent Encrypted message"))
        self.OnlineUser.setText(_translate("QMessenger", "#user234"))
        self.YourId.setText(_translate("QMessenger", "You"))
    #Call this function when you need to update the list of online users
    def sendData(self):
    def updateListOfOnlineUsers(self):
        self.inputs = self.encryptordata.inputs
        self.outputs = self.encryptordata.outputs
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QMessenger = QtWidgets.QMainWindow()
    ui = Ui_QMessenger()
    ui.setupUi(QMessenger)
    QMessenger.show()
    sys.exit(app.exec_())
