from queue import Queue
from queue import LifoQueue

class Singleton(type):
    '''Metaclass for the singleton'''
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class EncryptorData(metaclass=Singleton):
    '''
    Data to be shared with all the encryptor modules
    '''
    def __init__(self):
        '''constructor
        '''
        self.ut = Queue(0)
        self.good_ut = Queue(0)
        self.batchlist = {0:"file.csv"}
        self.node_list = []
        self.serversocket = None
        self.tdc_reader = ""
        self.hash_queue = Queue(0)
        self.save_data = Queue(0)
        self.hasher = ""
        self.goodkey = ""
        self.encrypt_key = "74"
        self.gps_reader = ""
        self.receiver=""
        self.sender=""
        self.hasher=""
        self.send_data=Queue(0)
        self.received_data=Queue(0)
        self.encrypt_socket=""
        self.receivedprocessor=""
        self.messenger=""
        self.encryptor=""
        self.ui=""
        self.gpstime=""
        self.gps_reader=""
        self.sendprocessor=""
        self.inputs=[]
        self.outputs=[]
        self.loginServerInputs=[]
        self.loginServerOutputs=[]
        self.senddict={}
        self.receiveddict={}
        self.loginserversocket=None
        self.loginServer=None
        self.mymessenger_server_socket = None
        self.myec_server_socket = None
        self.filelist = []
        self.files=None          # to fill the filename
        self.MESSENGERPORT = 5010
        self.ECPORT = 5015
        self.networkthread = None
        self.ecthread={}
        self.messengerthread={}
        self.chatAreaDictionary = {}
        self.scrollAreaWidgetContents = None
        self.encryptorthread = {}
        self.displaymessage = {}
        self.sent_raw_message = {}
        self.received_raw_message = {}
        self.key = {}
        self.onlineUsers = {}
