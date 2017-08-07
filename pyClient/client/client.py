from parser import Parser

class Client(Parser) :
    def __init__( self, send2server ):
        self.send2server = send2server 

    def SendInitialLizeMsg(self) :
        helloMsg = b"(init teamname (version 15))"
        self.send2server(helloMsg)
        
    def receiveFromServer(self, msg  ):
        # print data

        if msg.startswith( "(init" ):
            self.ParseInitializeMsg( msg ) 
        else:
            import udpClient 
            udpClient.setDataReceiveCallback( None ) 
            pass
            raise Exception ( "unknow server command: " +  msg  )


    
        
