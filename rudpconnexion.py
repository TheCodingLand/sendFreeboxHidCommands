from time import time 

from constantsrudp import *
from socket import *
from rudppacket import *

class rudpConnection():
    def __init__(self, destAddr, isClient):
        self.destAddr = destAddr
        self.wait     = SYN_ACK if isClient else SYN
        self.pktId    = 0
        if not isClient: 
            self.accept = [SYN] #[SYN, DAT, FIN]
            self.time   = 0
            self.data   = ''
    
        def checkTime(self, time):
            if time - self.time > END_WAIT:
                return False
            return True

    def printConnection(self):
        print '[RUDP Connection]'
        print '\tdestAddr:', self.destAddr
        print '\tpktId   :', self.pktId
        print '\twait    :', self.wait
        try:
            print '\taccept  :', self.accep
            print '\ttime    :', self.time
            print '\tdata    :', self.data
        except:
            print 'NOT VALID'
            
            
class client(object):
    def __init__(self, address, port):
        self.socketip=address
        self.socketport=port
        self.skt = socket(AF_INET, SOCK_DGRAM) #UDP
        
        self.skt.connect((address,port))
        #self.skt.bind(('', srcPort)) #used for recv
        
    def connect(self):
        destIP = self.socketip
        destPort = self.socketport
        self.conn = rudpConnection(None, True)
        self.conn.destAddr = (destIP, destPort)
        self.skt.setblocking(0)
        #self.skt.settimeout(RTO)
        for i in xrange(MAX_RESND):
            try: 
                self.skt.sendto(encode(rudpPacket(SYN, self.conn.pktId)), self.conn.destAddr)
                print rudpPacket(SYN, self.conn.pktId)     ## For debugging
                
                while True:
                    recvData, addr = self.skt.recvfrom(MAX_DATA)
                    try: 
                        recvPkt = decode(recvData)
                        sendPkt = rudpProcessSwitch[recvPkt['pktType']](recvPkt, self.conn)
                        return True
                    except WRONG_PKT, KeyError: continue
            except timeout: continue
            except Exception as e : 
                print e.message
                print '[Handshaking] unexpected error occurs\n' ## For debugging
                return False
        raise MAX_RESND_FAIL()