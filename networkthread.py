'''This is a thread module, creates a listener thread, accepts connections,
receives data, and transfers data'''
import EncryptorData
import select, pickle
#from COMM.Encryptor import Encryptor
from threading import Thread, Event
from queue import Queue
import struct
#from UI.messenger import Messenger
#from twofish import Twofish
import datetime
class NetworkThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.encryptordata  = EncryptorData.EncryptorData()
        self.inputs = self.encryptordata.inputs
        self.outputs = self.encryptordata.outputs
        self.senddict = self.encryptordata.senddict
        self.receiveddict = self.encryptordata.receiveddict
        self.switch = Event()
        self.switch.clear()
        print(self.inputs)
        #self.encryptor = Encryptor(b'7744')

    def run(self):
        '''the following will be called when the thread starts'''
        while not self.switch.is_set():
            #print("in networkthread while")
            #print(self.inputs)
            readable, writable, exceptional = select.select(self.encryptordata.inputs, self.encryptordata.outputs, self.encryptordata.inputs, 1)
            #print("after select")
            #print("printing the readables {}".format(readable))
            for s in readable:
                if s is self.encryptordata.loginserversocket:
                    data = s.recv()
                    list = data.list
                    self.encryptordata.onlineUsers=list
                    pass
                    # accepts the connections
                    # create a errorchekgin thread
                elif s is self.encryptordata.mymessenger_server_socket:
                    conn, addr = s.accept()
                    self.encryptordata.inputs.extend([conn])
                    self.encryptordata.outputs.extend([conn])
                    #for setting the socket to non-blocking
                    conn.setblocking(0)
                    pass
                    # accept the connections
                    #create a messengerthread
                else:
                    data = self.recv_msg(s)
                    socport = s.getsockname()[1]
                    peerport = s.getpeername()[1]
                    print(data)
                    self.encryptordata.receiveddict[s].put(data)
                    data = pickle.loads(data)
                    key_id = data.key_id
                    enc_msg = data.enc_msg
                    key = self.encryptordata.key[key_id]
                    #tfh=Twofish(key.encode())
                    #msg = self.encryptor.decode(enc_msg, tfh)
                    msg =  enc_msg
                    self.encryptordata.received_raw_message[s].put("{} {}".format(key_id, enc_msg))
                    #decrypt
                    self.encryptordata.displaymessage[s].put(datetime.date.strftime(datetime.datetime.now(),'%m/%d-%H:%M:%S')+"\nBurchard: {}".format(msg.decode('utf-8')))

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
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(sock, msglen)

    def recvall(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data


    def off(self):
        '''this will be called to off the thread'''
        self.switch.set()
