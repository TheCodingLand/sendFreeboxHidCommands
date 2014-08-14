

from zeroconf import raw_input, ServiceBrowser, Zeroconf
import socket

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
def detect():
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
    return freebox