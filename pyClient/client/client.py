from parser import Parser
from serverparam import ServerParam 
from playerparam import PlayerParam 

class Client(Parser) :
    def __init__( self, send2server ):
        self.send2server = send2server 

    def SendInitialLizeMsg(self) :
        helloMsg = b"(init teamname (version 15))"
        self.send2server(helloMsg)
        
    def receiveFromServer(self, msg  ):
        # print data

        if msg.startswith( "(init " ):
            self.ParseInitializeMsg( msg ) 
        elif msg.startswith( "(server_param " ):
            ServerParam.instance().ParseFromServerMsg( msg[ len( "(server_param " ): -1 ]   ) 
        elif msg.startswith( "(player_param " ):
            PlayerParam.instance().ParseFromServerMsg( msg[ len( "(player_param " ): -1 ]   ) 
        elif msg.startswith( "(player_type " ) : 
            ServerParam.instance().ParsePlayerType(  msg[ len( "(player_type " ): -1 ]  )
        elif msg.startswith( "(sense_body " ) :
            self.ParseSense( msg  )
        else:
            self.ParseSight( msg  )
            # print ServerParam.instance().playerTypes 
            import udpClient 
            udpClient.setDataReceiveCallback( None ) 
            pass
            raise Exception ( "unknow server command: " +  msg  )


    
        
