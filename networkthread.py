'''This is a thread module, creates a listener thread, accepts connections,
receives data, and transfers data'''
import EncryptorData
import select, pickle, queue, socket
import re
from Crypto.Cipher import AES
import requests
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
#from COMM.Encryptor import Encryptor
from threading import Thread, Event
from queue import Queue

import struct
#from UI.messenger import Messenger
#from twofish import Twofish
import datetime
class NetworkThread(QThread):
    signal = pyqtSignal()
    def __init__(self):
        QThread.__init__(self)
        self.encryptordata  = EncryptorData.EncryptorData()
        self.inputs = self.encryptordata.inputs
        self.outputs = self.encryptordata.outputs
        self.senddict = self.encryptordata.senddict
        self.receiveddict = self.encryptordata.receiveddict
        self.switch = Event()
        self.switch.clear()
        #self.encryptor = Encryptor(b'7744')

    def run(self):
        '''the following will be called when the thread starts'''
        while not self.switch.is_set():
            readable, writable, exceptional = select.select(self.encryptordata.inputs, self.encryptordata.outputs, self.encryptordata.inputs, 1)
            #print("after select")
            #print("printing the readables {}".format(readable))
            for s in readable:
                if s is self.encryptordata.loginserversocket:
                    data = s.recv(1024)
                    print("Online Users are", pickle.loads(data))
                    for sockFromOnlineUsers in pickle.loads(data):
                        if str(self.encryptordata.loginserversocket.getsockname()) != str(sockFromOnlineUsers):
                            print("Socket is ",sockFromOnlineUsers)
                            host, port = str(sockFromOnlineUsers).split(",")
                            #print("LoginserverSocket is ",self.encryptordata.loginserversocket.getsockname(),"and SocketFrom online User is", sockFromOnlineUsers)
                            newsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                            sockHost = re.search("'(.+?)'", host).group(1)
                            sockPort = re.search("(.+?)\)",port).group(1)
                            try:
                                print("\n\n\n\n\t\t",port, "and the socket is", sockHost)
                                newsocket.connect((sockHost,int(5000)))
                            except Exception as e:
                                print("Got Exception while creating your own sockets manually from the incoming list of LoginServer \n",e)
                            print("this is your new socket", newsocket)
                            self.encryptordata.inputs.extend([newsocket])
                    self.signal.emit()
                    #self.encryptordata.ui.updateListOfOnlineUsers()
                    pass
                    # accepts the connections
                    # create a errorchekgin thread
                elif s is self.encryptordata.mymessenger_server_socket:
                    conn, addr = s.accept()
                    self.encryptordata.inputs.extend([conn])
                    self.encryptordata.outputs.extend([conn])
                    self.encryptordata.senddict[conn] = queue.Queue()
                    #for setting the socket to non-blocking
                    conn.setblocking(0)
                    pass
                    # accept the connections
                    #create a messengerthread
                else:
                    data = s.recv(1024)
                    message_list = pickle.loads(data)
                    raw_data = message_list[1]
                    self.encryptordata.ui.textEditForRecievedMessages.append(str(raw_data))
                    data = self.decryptMessage(message_list[1],int(message_list[0]))
                    data = data.decode('utf-8')
                    if data:
                        socketIp = str(s.getpeername()).split(",")
                        socketIp = re.search("'(.+?)'", str(socketIp)).group(1)
                        particularUsersChatArea = self.encryptordata.chatAreaDictionary.get(str(socketIp)+"ChatArea")
                        #particularUsersChatArea.setAlignment(QtCore.Qt.AlignLeft)
                        particularUsersChatArea.append("\n")
                        particularUsersChatArea.append(str(data))
                        #self.encryptordata.senddict[s].put(data)
                        if s not in self.encryptordata.outputs:
                            self.encryptordata.outputs.append(s)
                    else:
                        if s in  self.encryptordata.outputs:
                            self.encryptordata.outputs.remove(s)
                        self.encryptordata.inputs.remove(s)
                        s.close()
                        del self.encryptordata.senddict[s]
                    # self.encryptordata.receiveddict[s].put(data)
                    # data = pickle.loads(data)
                    # key_id = data.key_id
                    # enc_msg = data.enc_msg
                    # key = self.encryptordata.key[key_id]
                    # #tfh=Twofish(key.encode())
                    # #msg = self.encryptor.decode(enc_msg, tfh)
                    # msg =  enc_msg
                    # self.encryptordata.received_raw_message[s].put("{} {}".format(key_id, enc_msg))
                    # #decrypt
                    # self.encryptordata.displaymessage[s].put(datetime.date.strftime(datetime.datetime.now(),'%m/%d-%H:%M:%S')+"\nBurchard: {}".format(msg.decode('utf-8')))

    def decryptMessage(self,message,startPosition):
        key = ''
        with open('Quantum_Keys.txt','r') as f:
                keys = f.readlines()
                for i in range(int(startPosition)-1,int(startPosition)-1+16):
                    key = key + keys[i].replace("\n","")
        decryption_suite = AES.new(key.encode('utf-8'), AES.MODE_CBC, ('EncryptionOf16By').encode('utf-8'))
        return decryption_suite.decrypt(message)

    def send_msg(self, sock, msg):
        # Prefix each message with a 4-byte length (network byte order)
        print(len(msg))
        msg = struct.pack('>I', len(msg)) + msg
        sock.sendall(msg)

    def recv_msg(self, sock):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(sock, 4)
        if not raw_msglen:
            return None
        # msglen = struct.unpack('>I', raw_msglen)[0]
        return raw_msglen
        # Read the message data
        return self.recvall(sock, msglen)

    def recvall(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        # data = b''
        # while len(data) < n:
        #     packet = sock.recv(n - len(data))
        #     if not packet:
        #         return None
        #     data += packet
        return sock.recv(4)


    def off(self):
        '''this will be called to off the thread'''
        self.switch.set()
