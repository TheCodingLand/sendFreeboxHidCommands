import re

import socket
import detectserver
import time
import binascii
import struct
servers = []
from constantsrudp import *
import rudpconnexion as	rudp





def interpretCommand(value):
	if value[0] >= 16:
		print value[0]
		return 'RUDP_CMD_APP'
	else:
		return COMMANDS[value[0]]
	 

    

class FoilsProtocolCheat(object):
	def __init__(self):
	
		self.devicename = "MonscriptDeLaMortRudpFoilsWTF"
		self.devicename = "74656C65636F6D6D616E6465207363726970742066726565626F7800000000000000000000000000000000000000000000000000000000000000000000000000"
		self.deviceSerial="JustCauseILikeDaTAInFIelds1337"
		self.deviceSerial= "00"*32
		self.reserved = "00"
		self.deviceVersion= "02"
		self.descriptorBlobOffset = "70" 
		self.descriptorBlobSize = "5b"
		self.descriptorPhysicalOffset = "cB" 
		self.descriptorPhysicalSize = "00"
		descriptorStringOffset = "cB"
		descriptorStringSize= "00"
		self.deviceDesciptor = "050C0901A1010902A10205091901290A1501250A750495018100C0050C098609E015FF250175029502814609E2093009340960096409830981150125077504950181000980A1020509190129031501250375028100C015028103C0"



def parseFoilsDeviceNew(packet):#to reverse with a set structured in a class 
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


class rudpSession():
	def init(self):
		self.ackSent = 0
		self.ackRecieved = 0
		self.queue = []
	def send(self, data):
		send(data)
		self.ackSent = self.ackSent+1
  	

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
	print "data : " + packet[16:]  
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


if __name__ == '__main__':
    freebox = detectserver.detect()
    
    print freebox.name
    print freebox.address
    print freebox.port
    
    print "connecting :" 
    rudpConnexion= rudp.client(freebox.address,int(freebox.port))
    rudpConnexion.connect()
    #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #sock.connect((freebox.address,int(freebox.port)))
    #sock.setblocking(0)
    
    
    
    
    while True:
        input = raw_input("input an hex packet of type 'handshake', and then 'descriptor':")
        if input == 'descriptor':
            input = testdescriptor
        if input == 'handshake':
        	input = testhandshake
     	hexString = input.replace(' ','').replace(':','') #allow all type of copy and paste
      	
    	parseRudpPacket(hexString)
    	print "sent :" + hexString
    	print "----------------------------------------------------------------"
    
     	rudpConnexion.skt.send(hexString.decode('hex'))
    	time.sleep(1)
        try:
            received = rudpConnexion.skt.recv(512)
            data= repr(received.encode("hex"))
            parseRudpPacket(data[1:])
            
        except socket.error:
            continue

    sock.close()
    

