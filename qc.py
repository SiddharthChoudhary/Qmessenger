# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qc.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QAction, QInputDialog, QLineEdit
from threading import Thread
import EncryptorData
import socket
import sys, re
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
class Ui_QMessenger(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_QMessenger,self).__init__()
        Ui_QMessenger.EXIT_CODE_REBOOT = -12345678 
        self.currentUser   = None
        self.encryptorData = EncryptorData.EncryptorData()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0',5000))
        self.server.listen(5)
        self.encryptorData.mymessenger_server_socket = self.server
        self.encryptorData.inputs.extend([self.encryptorData.mymessenger_server_socket])
        self.newfont = QtGui.QFont("Times", 12) 
        self.loginServer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.loginServer.connect((loginServerIp,3490))
        self.encryptorData.loginserversocket = self.loginServer
        self.encryptorData.inputs.extend([self.encryptorData.loginserversocket])
        self.onlineUsersList = []
        self.setForUniqueIpAddress = set()
    def setupUi(self, QMessenger):
        QMessenger.setObjectName("QMessenger")
        QMessenger.resize(1280, 800)
        QMessenger.closeEvent = self.closeEvent
        # Quit flag
        self.centralwidget = QtWidgets.QWidget(QMessenger)
        self.centralwidget.setObjectName("centralwidget")

        self.MessageArea = QtWidgets.QScrollArea(self.centralwidget)
        self.MessageArea.setGeometry(QtCore.QRect(20, 90, 750, 700))
        self.MessageArea.setWidgetResizable(True)
        self.MessageArea.setObjectName("MessageArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 698, 698))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.encryptorData.scrollAreaWidgetContents =  self.scrollAreaWidgetContents

        self.IntroLabel = QtWidgets.QLabel(self.centralwidget)
        self.IntroLabel.setGeometry(QtCore.QRect(10,20,1000,30))
        self.IntroLabel.setText("Chat with the Burchard Building User and see the encrypted and the decrypted messages ")
        self.IntroLabel.setFont(self.newfont)
        self.MessageArea.setWidget(self.scrollAreaWidgetContents)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 60, 80, 26))
        self.label_3.setFont(self.newfont)
        self.label_3.setObjectName("label_3")
    
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(20, 510, 1000, 300))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.ToSendText = QtWidgets.QPlainTextEdit(self.frame)
        self.ToSendText.setGeometry(QtCore.QRect(10, 200, 581, 62))
        self.ToSendText.setObjectName("ToSendText")
        self.ToSendText.keyPressEvent= self.keyPressEvent
        self.SendButton = QtWidgets.QPushButton(self.frame)
        self.SendButton.setGeometry(QtCore.QRect(620, 200, 91, 31))
        self.SendButton.setObjectName("SendButton")
        self.SendButton.clicked.connect(self.sendData)

        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(750, 47, 700, 750))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        #Vertical layouts for sending and recieving messages are defined here, also we are attaching textEdits to them as well
        self.verticalLayoutWidgetForSentMessages = QtWidgets.QWidget(self.frame_2)
        self.verticalLayoutWidgetForSentMessages.setGeometry(QtCore.QRect(29, 40, 300, 700))
        self.verticalLayoutWidgetForSentMessages.setObjectName("verticalLayoutWidget")

        self.verticalLayoutForSentMessages = QtWidgets.QVBoxLayout(self.verticalLayoutWidgetForSentMessages)
        self.verticalLayoutForSentMessages.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutForSentMessages.setObjectName("verticalLayoutForSentMessages")

        self.textEditForSentMessages = QtWidgets.QTextEdit(self.verticalLayoutWidgetForSentMessages)
        self.textEditForSentMessages.setObjectName("textEditForSentMessages")
        self.verticalLayoutForSentMessages.addWidget(self.textEditForSentMessages)
        self.textEditForSentMessages.setReadOnly(True)
        # self.SendEncryptedMessagelistView = QtWidgets.QListView(self.verticalLayoutWidget)
        # self.SendEncryptedMessagelistView.setObjectName("SendEncryptedMessagelistView")
        
        # self.encryptorData.SendEncryptedMessageBoxModel = QtGui.QStandardItemModel(self.SendEncryptedMessagelistView)
        # self.SendEncryptedMessagelistView.setModel(self.encryptorData.SendEncryptedMessageBoxModel)
        
        self.verticalLayoutWidgetForRecievedMessages = QtWidgets.QWidget(self.frame_2)
        self.verticalLayoutWidgetForRecievedMessages.setGeometry(QtCore.QRect(350, 40, 300, 700))
        self.verticalLayoutWidgetForRecievedMessages.setObjectName("verticalLayoutWidget_2")

        self.verticalLayoutForRecievedMessagesVBOXLAYOUT = QtWidgets.QVBoxLayout(self.verticalLayoutWidgetForRecievedMessages)
        self.verticalLayoutForRecievedMessagesVBOXLAYOUT.setContentsMargins(0, 0, 0, 0) 
        self.verticalLayoutForRecievedMessagesVBOXLAYOUT.setObjectName("verticalLayoutForSentMessages")

        self.textEditForRecievedMessages = QtWidgets.QTextEdit(self.verticalLayoutWidgetForRecievedMessages)
        self.textEditForRecievedMessages.setObjectName("textEditForRecievedMessages")
        self.verticalLayoutForRecievedMessagesVBOXLAYOUT.addWidget(self.textEditForRecievedMessages)
        self.textEditForRecievedMessages.setReadOnly(True)
        # self.RecieveEncryptedMessageListview = QtWidgets.QListView(self.verticalLayoutWidget_2)
        # self.RecieveEncryptedMessageListview.setObjectName("RecieveEncryptedMessageListview")
        

        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(380, 20, 210, 18))
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(self.newfont)
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setGeometry(QtCore.QRect(80, 20, 192, 18))
        self.label.setObjectName("label")
        self.label.setFont(self.newfont)
        self.onlineUsersArea = QtWidgets.QScrollArea(self.centralwidget)
        self.onlineUsersArea.setGeometry(QtCore.QRect(1500, 100, 366, 611))
        self.onlineUsersArea.setWidgetResizable(True)
        self.onlineUsersArea.setObjectName("onlineUsersArea")
        
        self.onlineUserLabel = QtWidgets.QLabel(self.centralwidget)
        self.onlineUserLabel.setObjectName("onlineUsersLabel")
        self.onlineUserLabel.setText("Online Users are")
        self.onlineUserLabel.setFont(self.newfont)
        self.onlineUserLabel.setGeometry(QtCore.QRect(1600,70,200,20))
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
        self.list.setGeometry(QtCore.QRect(0,0,364,364))
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
        self.YourId.setObjectName("Your Ip")
        self.YourId.setFont(self.newfont)
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
        QMessenger.setWindowTitle(_translate("QMessenger", "QMessenger Chat Application"))
        self.label_3.setText(_translate("QMessenger", "Messages"))
        self.ToSendText.setToolTip(_translate("QMessenger", "<html><head/><body><p>Type your text here...</p></body></html>"))
        self.SendButton.setText(_translate("QMessenger", "Send"))
        self.label_2.setText(_translate("QMessenger", "Recieved Encrypted message"))
        self.label.setText(_translate("QMessenger", "Sent Encrypted message"))
        #self.OnlineUser.setText(_translate("QMessenger", "#user234"))
        self.YourId.setText(_translate("QMessenger","Your Ip:"+str(socket.gethostbyname(socket.gethostname()))))
        self.updateListOfOnlineUsers()

    def keyPressEvent(self,e):
        if len(self.ToSendText.toPlainText()) > 200 and e.key() != QtCore.Qt.Key_Backspace:
            e.ignore()
        elif e.key()  == QtCore.Qt.Key_Return :
            self.sendData()
        else:
            QtWidgets.QPlainTextEdit.keyPressEvent(self.ToSendText,e)
    def sendData(self):
        message = self.ToSendText.toPlainText()
        if self.currentUser is None:
           msg = QMessageBox(QMessenger)
           msg.setIcon(QMessageBox.Information)
           msg.setText("You haven't selected any user yet to chat with")
           msg.setInformativeText("Please click on any user from the right side of your Online User's list")
           msg.setWindowTitle("No User Selected")
           msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
           retval = msg.exec_()
        elif message is None:
            msg = QMessageBox(QMessenger)
            msg.setIcon(QMessageBox.Information)
            msg.setText("Empty Messages not allowed")
            msg.setStandardButtons(QMessageBox.Ok)
        else:
            ##print("size of output list is ", self.encryptorData.inputs)
            for o in self.encryptorData.inputs:
                if (o is not self.encryptorData.mymessenger_server_socket) and (o is not self.encryptorData.loginserversocket):
                    host, port = str(o.getpeername()).split(",")
                    sockHost = str(re.search("'(.+?)'", host).group(1))
                    if sockHost in self.currentUser:
                        #encrypt message
                        particularUserschatArea = self.encryptorData.chatAreaDictionary.get(sockHost+"ChatArea")
                        #particularUserschatArea.setAlignment(QtCore.Qt.AlignRight)
                        particularUserschatArea.append(str(message).strip())
                        cursor = particularUserschatArea.textCursor()
                        textBlockFormat = cursor.blockFormat()
                        textBlockFormat.setAlignment(QtCore.Qt.AlignRight)
                        cursor.mergeBlockFormat(textBlockFormat)
                        particularUserschatArea.setTextCursor(cursor)
                        self.ToSendText.clear()
                        message = self.encryptMessage(message)
                        #print("I came in")
                        self.textEditForSentMessages.append(str(message[1]))
                        #print("I came in this after textEditS")
                        #print("Message being sent is ",message)
                        ##print("Message encoded is", message.encode('utf-8'), "\n and the type is ", type(message))
                        o.send(pickle.dumps(message))
    #to encrypt the sending message by appending length to the encrypted message
    def closeEvent(self,event):
        text,okPressed = QInputDialog.getText(QMessenger,"Enter Password","Enter Password to close the application", QLineEdit.Normal)
        if okPressed and text == 'Stevens#!46%':
            event.accept()
        else:
            event.ignore()
            msg = QMessageBox(QMessenger)
            msg.setIcon(QMessageBox.Information)
            msg.setText("Wrong Password")
            msg.setStandardButtons(QMessageBox.Ok)
            returnedValue = msg.exec_()
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
           # #print("I got hit 1", type(message))
            encrypted_message = str(startPosition)+':'
            #print("I got hit 2")
            with open('Quantum_Keys.txt','r') as f:
                keys = f.readlines()
                for i in range(startPosition-1,startPosition-1+16):
                    key = key + keys[i].replace("\n","")
            #print("Length of the original message is ", len(message.encode('utf-8')))
            if len(message.encode('utf-8'))%16!=0:
                while len(message.encode('utf-8'))%16!=0:
                    message = " "+ message
            encryption_suite = AES.new(key.encode('utf-8'), AES.MODE_CBC, ('EncryptionOf16By').encode('utf-8'))
            #print("Message is something like this", message)
            cipher_text = encryption_suite.encrypt(message.encode('utf-8','ignore'))
            ##print("Length of the cipher_text is ",len(cipher_text), "With cipher text ",cipher_text)
            ##print("Length of the string cipher text is ", len(str(cipher_text))," with cipher text now is ", str(cipher_text))
            encrypted_message_list  = [int(startPosition),cipher_text]
            #print("Encrypted message list is", encrypted_message_list)
            return encrypted_message_list
        except Exception as e:
            print("Got exception while encrypting, restarting the window now",e)
            #QtGui.qApp.exit( Ui_QMessenger.EXIT_CODE_REBOOT )
    def updateListOfOnlineUsers(self):
        print("List object is ", self.encryptorData.onlineUsers," and the inputs is ", self.encryptorData.inputs)
        
        for s in self.encryptorData.inputs:
            if s is self.encryptorData.loginserversocket:
                pass
            elif s is self.encryptorData.mymessenger_server_socket:
                #If it's you
                pass
            else:
                socketName = s.getpeername() if s.getpeername() else s.getsockname()
                host, port = str(socketName).split(",")
                sockHost = re.search("'(.+?)'", host).group(1)
                #only gets executed if this is a new user, i.e., there is no chatAreaDictionary already there for this
                if str(sockHost)+"ChatArea" not in self.encryptorData.chatAreaDictionary:
                    chatAreaObject = QtWidgets.QTextEdit()
                    chatAreaObject.setParent(self.scrollAreaWidgetContents)
                    chatAreaObject.setReadOnly(True)
                    chatAreaObject.setGeometry(QtCore.QRect(0, 0, 750, 700))
                    chatAreaObject.setObjectName(sockHost+"ChatArea")
                    self.encryptorData.chatAreaDictionary[chatAreaObject.objectName()] = chatAreaObject
                    self.onlineUsersList.append(sockHost)
                    self.setForUniqueIpAddress.add(sockHost)
                elif str(sockHost)+"ChatArea" in self.encryptorData.chatAreaDictionary:
                    self.setForUniqueIpAddress.add(sockHost)
                #If some socket goes down then we need to remove it from the inputs
        self.list.clear()
        print("online users list is ",self.onlineUsersList, "and ", self.setForUniqueIpAddress)
        for i in self.onlineUsersList:
            sockHostNew = i
            if sockHostNew in self.setForUniqueIpAddress:
                self.list.addItem(str(i))
                self.setForUniqueIpAddress.remove(sockHostNew)
        self.outputs = self.encryptorData.outputs

    def itemClickedOnList(self,item):
        self.currentUser = item.text()
        for i in self.encryptorData.chatAreaDictionary:
            #print("The dictionary is ", self.encryptorData.chatAreaDictionary)
            if i is not item.text()+"ChatArea":
                self.encryptorData.chatAreaDictionary.get(i).hide()
        particularUserschatArea = self.encryptorData.chatAreaDictionary.get(item.text()+"ChatArea")
        particularUserschatArea.show()
        # #print("Size is",self.encryptorData.chatAreaDictionary)
        # if item.text() in self.encryptorData.chatAreaDictionary:
        #     if item.text() is not None:
        #         self.verticalLayout = self.encryptorData.chatAreaDictionary[item.text()]
        #     else:

        #verticalLayout.addWidget(chatAreaObject)
        #self.encryptorData.chatAreaDictionary[item.text()] = verticalLayout
        # else:
        #     #print("It's not synchronised")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QMessenger = QtWidgets.QMainWindow()
    QMessenger.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    screen = app.primaryScreen()
    QMessenger.setFixedSize(screen.size().width(),screen.size().height())
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
