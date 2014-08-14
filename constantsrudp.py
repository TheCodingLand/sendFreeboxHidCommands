
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

     
FLAG = { 0: 'None',
         
         1 : 'ACK',
         2 : 'RELIABLE',
         3 : 'ACK and RELIABLE',
         4 : 'RETRANSMITTED', 
         5 : 'RETRANSMITTED And ACK',
         7 : 'RELIABLE AND RETRANSMITTED' ,
         8 : 'UNRELIABLE',
         9 : 'UNRELIABLE And ACK',
         11 : 'UNRELIABLE AND RETRNASMITTED',
         }