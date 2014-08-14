import time
import select
import sys
import logging
TIMEOUT = 1
CLOSED = 2
FD = 1
TIME = 2

events = []
logger = logging.logger("EVENT", logging.DEBUG)


def getCurrentMills():
    return int(round(time.time() * 500))

def eventTimeout(timeMs, callback, argument, strId):    
    event = EventData(TIME, callback, argument)
    event.time = getCurrentMills() + timeMs
    event.id = strId
    logger.log(Level.DEBUG, "Registering timeout " + str(event)) 
    events.append(event)

def eventTimeoutDelete(callback, argument):
    for event in events:
        if event.type == TIME and event.callback == callback and event.argument == argument:
            logger.log(Level.DEBUG, "Deleting " + str(event))
            events.remove(event)
            return True
    return False

def eventFd(fd, callback, callbackArgument, strId):
    logger.log(Level.DEBUG, "FD Registered fd:" + str(fd))
    event = EventData(EVENT_TYPE_FD, callback, callbackArgument)
    event.fd = fd
    event.id = strId
    events.append(event)
    pass

def eventFdDelete(callback, argument):
    for event in events:
        if event.type == EVENT_TYPE_FD and event.callback == callback and event.argument == argument:
            events.remove(event)
            return True
    return False

def eventLoop():
    LOOP_DELAY = 0.001
    while True:
        if len(events) < 1:
            break
        for event in events:
            if event.type == EVENT_TYPE_FD :
                #print "Found:" + str(event)
                # Check if we have some data available
                oRead, [],  [] = select.select([event.fd], [], [], 0) # 0 - means polling, othewrise timeout time in seconds
                if len(oRead) > 0:
                    event.callback(event.fd, event.argument)
                else:
                    #sys.stdout.write('.')
                    time.sleep(LOOP_DELAY)
            elif event.type == EVENT_TYPE_TIME:
                logger.log(Level.DEBUG,"Checking for timeout, current time:" + str(getCurrentMills()) + " event timeout:" + str(event.time) + " id:" + str(event.id))
                if event.time < getCurrentMills():
                    logger.log(Level.ERROR, "\n\nTIMEOUT for event: " + str(event)) 
                    event.callback(event.argument)

class EventData:
    def __init__(self, eventType, eventCallback, eventArgument):           
        self.type = eventType
        self.callback = eventCallback
        self.argument = eventArgument
        self.fd = None # to be set outside constructor
        self.time = None # to be set outside constructor
        self.id = None
    def __str__(self):  # Override string representation
        return "Type:" + str(self.type) + " argument:" + str(self.argument) + " callback:" + str(self.callback)