import re

import socket
from zeroconf import raw_input, ServiceBrowser, Zeroconf
import time
import binascii
import struct
servers = []
	
class Server(object):
	def __init__(self, address, port, name):
	    self.address = address
	    self.port = port
	    self.name = name
		
	
class MyListener(object):

    def addService(self, zeroconf, type, name):
        info = zeroconf.getServiceInfo(type, name)
        if info:
            servers.append(Server(socket.inet_ntoa(info.getAddress()),
                                          info.getPort(),info.getServer() ))
            prop = info.getProperties()




FOILS_COMMANDS = { 0 : 'FOILS_HID_DEVICE_NEW', # client to server
    			 1 : 'FOILS_HID_DEVICE_DROPPED', # client to server
	       		 2 : 'FOILS_HID_DEVICE_CREATED', # server to client
    	      	 3 : 'FOILS_HID_DEVICE_CLOSE', # server to client
    			 4 : 'FOILS_HID_FEATURE', # bidir
        		 5 : 'FOILS_HID_DATA', # bidir
     	     	 6 : 'FOILS_HID_GRAB', # server to client
     	 	     7 : 'FOILS_HID_RELEASE', # server to client
    	 	 	 8 : 'FOILS_HID_FEATURE_SOLLICIT' } # server to client

COMMANDS = { 0 : 'RUDP_CMD_NOOP',
			 1 : 'RUDP_CMD_CLOSE',
    	 	 2 : 'RUDP_CMD_CONN_REQ',
    	 	 3 : 'RUDP_CMD_CONN_RSP',
    	 	 4 : 'RUDP_CMD_PING',
    	 	 5 : 'RUDP_CMD_PONG' }


def interpretCommand(value):
	if value[0] >= 16:
		print value[0]
		return 'RUDP_CMD_APP'
	else:
		return COMMANDS[value[0]]
	 

     	
FLAG = { 1 : 'ACK',
	     2 : 'RELIABLE',
	     3 : 'ACK and RELIABLE',
    	 4 : 'RETRANSMITTED', 
    	 5 : 'RETRANSMITTED And ACK',
    	 7 : 'RELIABLE AND RETRANSMITTED' ,
    	 8 : 'UNRELIABLE',
    	 9 : 'UNRELIABLE And ACK',
    	 11 : 'UNRELIABLE AND RETRNASMITTED',
    	 }

class FoilsProtocolCheat(object):
	def __init__(self):
	
		self.devicename = "MonscriptDeLaMortRudpFoilsWTF"
		self.deviceSerial = "JustCauseILikeDaTAInFIelds1337"
		self.deviceVersion = 0x00

    #self.remoteDescriptor = structDescriptor.pack()

def parseFoilsDeviceNew(packet):
	    deviceName = packet[0:128]
	    print "deviceName" + str(deviceName)
	    deviceSerial = packet[128:192]
	    print "deviceSerial" + str(deviceSerial)
	    reserved = int(packet[192:196], 16)
	    deviceVersion =int(packet[196:198], 16)
	    print "deviceVersion" + str(deviceVersion)
	    descriptorBlobOffset = int(packet[200:204], 16)
	    print "deviceBlobOffset" + str(descriptorBlobOffset)
	    descriptorBlobSize = int(packet[204:208], 16)
	    print "deviceBlobSize" + str(descriptorBlobSize)
	    descriptorPhysicalOffset = int(packet[208:212], 16)
	    descriptorPhysicalSize = int(packet[212:216], 16)
	    descriptorStringOffset = int(packet[216:220], 16)
	    descriptorStringSize = int(packet[220:224], 16)
	    print "Device Report Descriptor : %s" % packet[descriptorBlobOffset*2:descriptorBlobOffset*2+descriptorBlobSize*2 ]



def parseRudpPacket(packet):

	#command = int(packet[0:5])
     	
	print "data :" +packet
	print "command :" + packet[0:2] + ' ' + interpretCommand([int(packet[0:2], 16)])
	print repr(binascii.unhexlify(packet[2:4]))
	
	print "FLAG : " + FLAG[int(packet[2:4],16)]
	packet[4:6]
	headerLgt = int(packet[2:4], 16)
	ACKRELIABLE= packet[4:8]
	RELIABLESEQ = packet[8:12]
	UNRSEQ = packet[12:16]
	print "ACKRELIABLE :"+ ACKRELIABLE
	print "RELIABLESEQ :" + RELIABLESEQ
	print "UNRSEQ :" + UNRSEQ  
	parseFoilsHeader(packet[16:])

			 
def parseFoilsHeader(packet):
	deviceID = packet[0:8]
	report = packet[8:16]
	if len(packet) ==8:
		print "Handshake"
	else:
		try:
			report = int(report, 16) 
			parseFoilsDeviceNew(packet[16:])
		except:
			print "no FOILS DATA"
		
		#===========================================================================
	# print "opt :" + packet[2:4] + OPTS[int(packet[2:4])]
	# 	#print "data (hid?) :"+ data[5:]
	# print "looks like a device id [" + packet[4:8]+ ":" + packet [8:12] + "]"
	# print "report id : " + packet[12:16]
	#===========================================================================
#===============================================================================
#     
# def parseFoilsPacket(packet):
#     print "data :" +packet
#     print "command :" + packet[0:2] + COMMANDS[int(packet[0:2])]
#     print "opt :" + packet[2:4] + OPTS[int(packet[2:4])]
#     #print "data (hid?) :"+ data[5:]
#     print "unknown data:" + packet[4:8]
#     print "device id : [" + packet [8:12] + "]"
#     print "report id : " + packet[12:16]
#===============================================================================
    #print "Foils command :" + FOILS_COMMANDS[int(packet[16:20])]


if __name__ == '__main__':
    zeroconf = Zeroconf()
    print("Browsing services...")
    listener = MyListener()
    browser = ServiceBrowser(zeroconf, "_hid._udp.local.", listener)
    freebox=False
    while freebox==False: 
   
    	for server in servers:
    		if 'Freebox' in server.name:
    			freebox=server
    zeroconf.close()
    
    print freebox.name
    print freebox.address
    print freebox.port
    
    print "connecting :" 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((freebox.address,int(freebox.port)))
    sock.setblocking(0)
    
    while True:
    	
    	
    	
    	
    	
    	
        input = raw_input("input an hex packet:")
    	#hexArray = re.findall('..',input.replace(' ','').replace(':',''))
     	hexString = input.replace(' ','').replace(':','')
      	#for hex in hexArray:
    	#   chrVal= chr(int(hex, 16))
    	#   hexString = hexString + chrVal  
    	
    	parseRudpPacket(hexString)
    	print "sent :" + hexString
    	print "----------------------------------------------------------------"
    	
    	
    	
    
     	sock.send(hexString.decode('hex'))
        #02010000bd980000d8aec240
    	time.sleep(1)
        try:
            received = sock.recv(512)
            data= repr(received.encode("hex"))
            parseRudpPacket(data[1:])
            
        except socket.error:
            continue
    	#received = sock.recv(1024)
    	
    	
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
    	
    	
     	
     	
     	
     	
    
    
    sock.close()
    

