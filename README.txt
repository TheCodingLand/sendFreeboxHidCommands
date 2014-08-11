FOILS or is an api that has been implemented on the french provider media player.

it allows HID like communication, so keyboards, mices, remote controls etc...

The protocol is described here :
http://dev.freebox.fr/sdk/foils_hid/#_Protocol

This script's goal is just to send and recieve commands, to test and understand the protocol.

More info on the API is available here : 
http://dev.freebox.fr/sdk/

Installation :

First, install Python 2.7

Open a command prompt :

"pip install zeroconf"

and 

"python send sendHidCommandsFbx.py" 

paste hex values for the packets you want to try

ex : 
02010000bd980000d8aec240

The box should send a reply.

For devs only until we can figure out what the FBX should reply and what to send it back.

For now, this script does nothing usefull except for devs.

Oh, and this descriptor should work :
100100001D390000000000020000000054C3A96CC3A9636F6D6D616E6465204672656554C3A96C65630000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000070005000C0000000C00000050C0901A10185019501751019002A8C021500268C0280C005010906A1018502050795017508150026FF00050719002AFF0080C005010A8000A1018503750195041A81002A84008102750195048101C00000000000000000

cheers.