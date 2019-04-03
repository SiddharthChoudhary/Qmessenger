# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qc.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from threading import Thread
import EncryptorData
import socket
import sys
import select
from Crypto.Cipher import AES
import requests
import signal
from threading import Thread
from networkthread import *
ChatArea={}
server=None
dataTobeSent = None
loginServerIp="155.246.65.190"
class Ui_QMessenger(object):
    def __init__(self):
        Ui_QMessenger.EXIT_CODE_REBOOT = -12345678 
        self.currentUser   = None
        self.encryptorData = EncryptorData.EncryptorData()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0',5000))
        self.server.listen(5)
        self.encryptorData.mymessenger_server_socket = self.server
        self.encryptorData.inputs.extend([self.encryptorData.mymessenger_server_socket])
        self.loginServer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.loginServer.connect((loginServerIp,3490))
        self.encryptorData.loginserversocket = self.loginServer
        self.encryptorData.inputs.extend([self.encryptorData.loginserversocket])
    def setupUi(self, QMessenger):
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
        self.encryptorData.scrollAreaWidgetContents =  self.scrollAreaWidgetContents

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

        #Vertical layouts for sending and recieving messages are defined here, also we are attaching textEdits to them as well
        self.verticalLayoutWidgetForSentMessages = QtWidgets.QWidget(self.frame_2)
        self.verticalLayoutWidgetForSentMessages.setGeometry(QtCore.QRect(29, 40, 161, 391))
        self.verticalLayoutWidgetForSentMessages.setObjectName("verticalLayoutWidget")

        self.verticalLayoutForSentMessages = QtWidgets.QVBoxLayout(self.verticalLayoutWidgetForSentMessages)
        self.verticalLayoutForSentMessages.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutForSentMessages.setObjectName("verticalLayoutForSentMessages")

        self.textEditForSentMessages = QtWidgets.QTextEdit(self.verticalLayoutWidgetForSentMessages)
        self.textEditForSentMessages.setObjectName("textEditForSentMessages")
        self.verticalLayoutForSentMessages.addWidget(self.textEditForSentMessages)

        # self.SendEncryptedMessagelistView = QtWidgets.QListView(self.verticalLayoutWidget)
        # self.SendEncryptedMessagelistView.setObjectName("SendEncryptedMessagelistView")
        
        # self.encryptorData.SendEncryptedMessageBoxModel = QtGui.QStandardItemModel(self.SendEncryptedMessagelistView)
        # self.SendEncryptedMessagelistView.setModel(self.encryptorData.SendEncryptedMessageBoxModel)
        
        self.verticalLayoutWidgetForRecievedMessages = QtWidgets.QWidget(self.frame_2)
        self.verticalLayoutWidgetForRecievedMessages.setGeometry(QtCore.QRect(220, 40, 160, 391))
        self.verticalLayoutWidgetForRecievedMessages.setObjectName("verticalLayoutWidget_2")

        self.verticalLayoutForRecievedMessagesVBOXLAYOUT = QtWidgets.QVBoxLayout(self.verticalLayoutWidgetForRecievedMessages)
        self.verticalLayoutForRecievedMessagesVBOXLAYOUT.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutForRecievedMessagesVBOXLAYOUT.setObjectName("verticalLayoutForSentMessages")

        self.textEditForRecievedMessages = QtWidgets.QTextEdit(self.verticalLayoutWidgetForRecievedMessages)
        self.textEditForRecievedMessages.setObjectName("textEditForSentMessages")
        self.verticalLayoutForRecievedMessagesVBOXLAYOUT.addWidget(self.textEditForRecievedMessages)
        # self.RecieveEncryptedMessageListview = QtWidgets.QListView(self.verticalLayoutWidget_2)
        # self.RecieveEncryptedMessageListview.setObjectName("RecieveEncryptedMessageListview")
        

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
        self.RefreshButton = QtWidgets.QPushButton(self.onlineUsersArea)
        self.RefreshButton.setGeometry(QtCore.QRect(120, 520, 113, 32))
        self.list = QtWidgets.QListWidget(self.onlineUsersArea)
        self.list.itemClicked.connect(self.itemClickedOnList)
        self.RefreshButton.setObjectName("RefreshButton")
        self.RefreshButton.setText("Refresh")
        self.RefreshButton.clicked.connect(self.updateListOfOnlineUsers)
        # self.OnlineUser = QtWidgets.QLabel(self.horizontalLayoutWidget)
        # self.OnlineUser.setAlignment(QtCore.Qt.AlignCenter)
        # self.OnlineUser.setObjectName("OnlineUser")
        # self.horizontalLayout.addWidget(self.OnlineUser)
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
        #self.OnlineUser.setText(_translate("QMessenger", "#user234"))
        self.YourId.setText(_translate("QMessenger", "You"))
        self.updateListOfOnlineUsers()
    def sendData(self):
        if self.currentUser is None:
           msg = QMessageBox()
           msg.setIcon(QMessageBox.Information)
           msg.setText("You haven't selected any user yet to chat with")
           msg.setInformativeText("Please click on any user from the right side of your User's list")
           msg.setWindowTitle("No User Selected")
           msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
           retval = msg.exec_()
        else:
            print("size of output list is ", self.encryptorData.outputs)
            for o in self.encryptorData.inputs:
                if (o is not self.encryptorData.mymessenger_server_socket) and (o is not self.encryptorData.loginserversocket):
                    if str(o.getpeername()) in self.currentUser:
                        print("getpeername is ", o.getpeername()," and ",self.currentUser)
                        message = self.ToSendText.toPlainText()
                        #encrypt message
                        socketIp = str(o.getpeername()).split(",")
                        socketIp =  re.search("'(.+?)'", socketIp).group(1)
                        particularUserschatArea = self.encryptorData.chatAreaDictionary.get(str(socketIp)+"ChatArea")
                        particularUserschatArea.setAlignment(QtCore.Qt.AlignRight)
                        particularUserschatArea.append(message)
                        self.ToSendText.clear()
                        message = self.encryptMessage(message)
                        print("I came in")
                        #self.textEditForSentMessages.append(str(message[1]))
                        print("I came in this after textEditS")
                        print("Message being sent is ",message)
                        #print("Message encoded is", message.encode('utf-8'), "\n and the type is ", type(message))
                        o.send(pickle.dumps(message))
    #to encrypt the sending message by appending length to the encrypted message
    def encryptMessage(self,message):
        #to get the random number so that I can start traversing through that point
        try:
            encrypted_message_list = []
            r = requests.get(url="http://quest.phy.stevens.edu:5050/main?lower=1&higher=194&amount=1")
            startPosition = r.json()['finalrandomarray'][0]
            key = ''
            #To calculate the start position from where we are going to start traversing in a file
            #if the startposition is greater than 194, i.e., minimum line number to be taken from a file then subtract it a bit
            if startPosition > 194:
                offsetAmount = startPosition-194
                startPosition= startPosition-offsetAmount
            #Read the quantum_keys file and then read 16 lines to generate a key of length 32 bytes, because each character is a byte
           # print("I got hit 1", type(message))
            encrypted_message = str(startPosition)+':'
            #print("I got hit 2")
            with open('Quantum_Keys.txt','r') as f:
                keys = f.readlines()
                for i in range(startPosition-1,startPosition-1+16):
                    key = key + keys[i].replace("\n","")
            print("Length of the original message is ", len(message.encode('utf-8')))
            if len(message.encode('utf-8'))%16!=0:
                while len(message.encode('utf-8'))%16!=0:
                    message = " "+ message
            encryption_suite = AES.new(key.encode('utf-8'), AES.MODE_CBC, ('EncryptionOf16By').encode('utf-8'))
            print("Message is something like this", message)
            cipher_text = encryption_suite.encrypt(message.encode('utf-8','ignore'))
            #print("Length of the cipher_text is ",len(cipher_text), "With cipher text ",cipher_text)
            #print("Length of the string cipher text is ", len(str(cipher_text))," with cipher text now is ", str(cipher_text))
            encrypted_message_list  = [int(startPosition),cipher_text]
            print("Encrypted message list is", encrypted_message_list)
            return encrypted_message_list
        except Exception as e:
            print("Got exception while encrypting, restarting the window now",e)
            #QtGui.qApp.exit( Ui_QMessenger.EXIT_CODE_REBOOT )
    def updateListOfOnlineUsers(self):
        print("List object is ", self.encryptorData.onlineUsers," and the inputs is ", self.encryptorData.inputs)
        onlineUsersList = []
        setForUniqueIpAddress = set()
        for s in self.encryptorData.inputs:
            if s is self.encryptorData.loginserversocket:
                pass
            elif s is self.encryptorData.mymessenger_server_socket:
                #If it's you
                pass
            else:
                print("The socket is ",s)
                if str(s.getpeername())+"ChatArea" not in self.encryptorData.chatAreaDictionary:
                    chatAreaObject = QtWidgets.QTextEdit()
                    chatAreaObject.setParent(self.scrollAreaWidgetContents)
                    chatAreaObject.setReadOnly(True)
                    chatAreaObject.setGeometry(QtCore.QRect(0, 0, 381, 391))
                    chatAreaObject.setObjectName(str(s.getpeername())+"ChatArea")
                    self.encryptorData.chatAreaDictionary[chatAreaObject.objectName()] = chatAreaObject
                    socketName = s.getpeername() if s.getpeername() else s.getsockname()
                    onlineUsersList.append(socketName)
                    host, port = str(socketName).split(",")
                    sockHost = re.search("'(.+?)'", host).group(1)
                    setForUniqueIpAddress.add(sockHost)
                #If some socket goes down then we need to remove it from the inputs
        self.list.clear()
        for i in onlineUsersList:
            sockHostNew = i
            if sockHostNew in setForUniqueIpAddress:
                self.list.addItem(str(i))
                setForUniqueIpAddress.remove(sockHostNew)
        self.outputs = self.encryptorData.outputs
        print("online users list is ",onlineUsersList)

    def itemClickedOnList(self,item):
        self.currentUser = item.text()
        for i in self.encryptorData.chatAreaDictionary:
            print("The dictionary is ", self.encryptorData.chatAreaDictionary)
            if i is not item.text()+"ChatArea":
                self.encryptorData.chatAreaDictionary.get(i).hide()
        particularUserschatArea = self.encryptorData.chatAreaDictionary.get(item.text()+"ChatArea")
        particularUserschatArea.show()
        # print("Size is",self.encryptorData.chatAreaDictionary)
        # if item.text() in self.encryptorData.chatAreaDictionary:
        #     if item.text() is not None:
        #         self.verticalLayout = self.encryptorData.chatAreaDictionary[item.text()]
        #     else:

        #verticalLayout.addWidget(chatAreaObject)
        #self.encryptorData.chatAreaDictionary[item.text()] = verticalLayout
        # else:
        #     print("It's not synchronised")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QMessenger = QtWidgets.QMainWindow()
    ui = Ui_QMessenger()
    EncryptorData.EncryptorData().ui = ui
    ui.setupUi(QMessenger)
    networkThread = NetworkThread()
    networkThread.start()
    networkThread.signal.connect(ui.updateListOfOnlineUsers)
    QMessenger.show()
    # currentExitCode = Ui_QMessenger.EXIT_CODE_REBOOT
    # while currentExitCode == Ui_QMessenger.EXIT_CODE_REBOOT:
    #     a = QtWidgets.QApplication(sys.argv)
    #     w = QtWidgets.QMainWindow()
    #     w.show()
    #     currentExitCode = a.exec_()
    #     a = None
    sys.exit(app.exec_())
