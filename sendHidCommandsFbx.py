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
    	hexArray = re.findall('..',input)
     	hexString = ""
      	for hex in hexArray:
    	   chrVal= chr(int(hex, 16))
    	   hexString = hexString + chrVal  
    	
 
    	print "sent :" + repr(hexString)
    
     	sock.send(hexString)
    #02010000bd980000d8aec240
    	time.sleep(1)
        try:
            received = sock.recv(512)
        except socket.error:
            continue
    	#received = sock.recv(1024)
     	
     	print "Received {}".format(repr(received))
    
    
    sock.close()
    

