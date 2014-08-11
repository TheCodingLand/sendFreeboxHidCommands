import re

import socket
from zeroconf import raw_input, ServiceBrowser, Zeroconf
import time
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


COMMANDS = { 0 : 'RUDP_CMD_NOOP',
			 1 : 'RUDP_CMD_CLOSE',
    	 	 2 : 'RUDP_CMD_CONN_REQ',
    	 	 3 : 'RUDP_CMD_CONN_RSP',
    	 	 4 : 'RUDP_CMD_PING',
    	 	 5 : 'RUDP_CMD_PONG',
    	 	 11 : 'RUDP_CMD_APP'
    	 			 }
OPTS = { 1 : 'ACK',
	     2 : 'RELIABLE',
    	 4 : 'RETRANSMITTED' }
     	


def parseRudpPacket(packet):
	
	

	#command = int(packet[0:5])
     	
    	 			
    		
     	
	print "recieved :" +packet
	print "command :" + packet[0:2] + COMMANDS[int(packet[0:2])]
	print "opt :" + packet[2:4] + OPTS[int(packet[2:4])]
	#print "data (hid?) :"+ data[5:]
	print "lookds like a device id [" + packet[4:8]+ ":" + packet [8:12] + "]"
	print "report id : " + packet[12:16]



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
    

