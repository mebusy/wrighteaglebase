from __future__ import print_function

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

server_host = '127.0.0.1'
server_port = 6000 

_callback_datagramReceived = None
_server_addr = None 


class Echo(DatagramProtocol):
    def startProtocol(self):
        pass
        
    def datagramReceived(self, data, addr):
        # print("received %r from %s" % (data, addr))
        # print( _callback_datagramReceived  )
        if _callback_datagramReceived is not None  :
            _callback_datagramReceived( data  )

        global _server_addr 
        if _server_addr is None :
            _server_addr = addr 


def startUDP():
    # 0 means any port, we don't care in this case
    t = reactor.listenUDP(0, Echo())
    
    def sendMsg( msg ) : 
        # global _server_addr 
        t.protocol.transport.write(  msg, ( server_host , server_port  ) if _server_addr is None else _server_addr   )
    return sendMsg 
    
def setDataReceiveCallback( callback  ):
    global _callback_datagramReceived
    _callback_datagramReceived = callback 


if __name__ == '__main__':
    send2server  = startUDP() 
    helloMsg = b"(init teamname (version 15))"
    send2server(helloMsg)

    reactor.run()
