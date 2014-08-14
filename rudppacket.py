
from struct import pack, unpack
from time import time 


from constantsrudp import *



        
#===============================================================================
# Low-level protocol is peer-to-peer. As UDP is not connected, one of the two involved peers must send a packet first. Any of the two can do it. This packet is expected to be containing a RUDP_CMD_CONN_REQ command with reliable sequence number to a random value.. This packet should be reliable, i.e. imply retransmits in the sender's code.
# Peer is expected to answer with an unreliable packet containing both an ACK and a RUDP_CMD_CONN_RSP packet. Its sequence number must be random as well. If the response packet is lost in transit, handshake will fail and must be started over. This is intended.
# After these two packets are exchanged, connection is established. Each peer takes the sequence number it received in first packet as granted. This is only true for first packet.
# 
# On an established connection, 3 main types of packets may transit:
# 
# - Ping/Pong packets
# 
# - Noop packets
# 
# - Data packets
#===============================================================================
        
        
         

    

def rudpPacket(pktType = None, pktId = None, data = ''):
    return {'pktType': pktType, 'pktId': pktId, 'data': data}


def processSYN(rudpPkt, c):
    if SYN in c.accept:
        if c.wait == SYN: c.accept += [DAT, FIN]
        c.pktId = rudpPkt['pktId'] + 1
        c.wait  = DAT
        c.time  = time()
        return rudpPacket(SYN_ACK, c.pktId)
    raise WRONG_PKT('processSYN', rudpPkt)
def processDAT(rudpPkt, c):
    if DAT == c.wait:
        if rudpPkt['pktId'] == c.pktId:
            if SYN in c.accept: c.accept.remove(SYN)
            c.pktId += 1
            c.data  += rudpPkt['data']
            c.time   = time() 
            return rudpPacket(ACK, c.pktId)
        elif rudpPkt['pktId'] == c.pktId - 1: 
            c.time   = time()
            return rudpPacket(ACK, c.pktId)
        elif rudpPkt['pktId'] < c.pktId - 1: raise WRONG_PKT('processDAT [Duplicated]', rudpPkt) # Bugs
    raise WRONG_PKT('processDAT', rudpPkt)
def processFIN(rudpPkt, c):
    if FIN in c.accept and rudpPkt['pktId'] == c.pktId:
        if DAT in c.accept: c.accept.remove(DAT)
        c.wait = FIN
        c.time = time()
        return rudpPacket(FIN_ACK, c.pktId + 1)
    raise WRONG_PKT('processFIN', rudpPkt)



def processSYN_ACK(rudpPkt, c):
    if SYN_ACK == c.wait and rudpPkt['pktId'] == c.pktId + 1:
        c.wait = ACK
        c.pktId += 1
        return rudpPacket(DAT, c.pktId)
    raise WRONG_PKT('processSYN_ACK', rudpPkt)
def processACK(rudpPkt, c):
    if ACK == c.wait and rudpPkt['pktId'] == c.pktId + 1:
        c.pktId += 1
        return rudpPacket(DAT, c.pktId)
    raise WRONG_PKT('processACK', rudpPkt)
def processFIN_ACK(rudpPkt, c):
    if FIN_ACK == c.wait and rudpPkt['pktId'] == c.pktId + 1:
        c.pktId += 1
        raise END_CONNECTION(c)
    raise WRONG_PKT('processFIN_ACK', rudpPkt)

#rudpProcessSwitch[rudpPkt['pktType']](rudpPkt, c) <-- how you use process functions
rudpProcessSwitch = {SYN: processSYN, SYN_ACK: processSYN_ACK, DAT: processDAT, ACK: processACK, FIN: processFIN, FIN_ACK: processFIN_ACK}
#-------------------#
# Protocol codec    #
#-------------------#
def encode(rudpPkt): #pktId can be either ACK # or SEQ #
    if rudpPkt['pktId'] <= MAX_PKTID:
        header = rudpPkt['pktType'] | rudpPkt['pktId']
        return pack('i', header) + rudpPkt['data']
    raise ENCODE_DATA_FAIL()

def decode(bitStr):
    if len(bitStr) < 4:
        raise DECODE_DATA_FAIL()
    else:
        header  = unpack('i', bitStr[:4])[0]
        return rudpPacket(header & 0x7f000000, header & 0x00ffffff, bitStr[4:])
