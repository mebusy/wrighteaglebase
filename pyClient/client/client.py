from parser import Parser
from serverparam import ServerParam 
from playerparam import PlayerParam 
from rcss import PM_BeforeKickOff  , PM_PlayOn , PM_KickOff_Left
from readlisp import writelisp ,  getCmdSymbol
import random  , math 


class Client(Parser) :
    def __init__( self, send2server ):
        super( Client , self ).__init__() 
        self.__send2server = send2server 
        self.__debugTick = 0

    def sendMsg( self, msg ) :
        self.__send2server( msg + '\0' )


    def SendInitialLizeMsg(self) :
        helloMsg = b"(init teamname (version 15))" 
        self.sendMsg( helloMsg  )
        
    def receiveFromServer(self, msg  ):
        # print data

        if msg.startswith( "(init " ):
            self.ParseInitializeMsg( msg ) 
        elif msg.startswith( "(server_param " ) or msg.startswith( "(player_param " ) :
            if msg.startswith( "(server_param " ) :
                ServerParam.instance().ParseFromServerMsg( msg[ len( "(server_param " ): -1 ]   ) 
            else:
                PlayerParam.instance().ParseFromServerMsg( msg[ len( "(player_param " ): -1 ]   ) 

            if PlayerParam.instance().paramsFromServer is not None and ServerParam.instance().paramsFromServer is not None :   
                ServerParam.instance().initParamFromServer()
                self.observer.Initialize()
                     

        elif msg.startswith( "(player_type " ) : 
            ServerParam.instance().ParsePlayerType(  msg[ len( "(player_type " ): -1 ]  )
        elif msg.startswith( "(sense_body " ) :
            self.ParseSense( msg  )
        elif msg.startswith( "(see " ) :
            self.ParseSight( msg  )
        elif msg.startswith( "(hear " ):
            self.ParseSound( msg )

        elif msg.startswith( "(warning " ) :
            print msg 
        else:
            # print ServerParam.instance().playerTypes 
            import udpClient 
            udpClient.setDataReceiveCallback( None ) 
            pass
            raise Exception ( "unknow server command: " +  msg  )

    def plan( self ) :
        if not self.observer.initialized:
            return 

        if self.observer.serverPlayMode == PM_BeforeKickOff  : 
            # x = random.uniform( 0, ServerParam.instance().PITCH_LENGTH/2.0 ) 
            # y = random.uniform( -ServerParam.instance().PITCH_WIDTH/2.0 , ServerParam.instance().PITCH_WIDTH/2.0 ) 
            # if self.observer.needRotate:
            #     x *= -1
            # self.exec_moveTo( x,y )
            self.exec_moveTo( -0.5 , 0 )
            return 
        if self.observer.serverPlayMode == PM_KickOff_Left :
            self.exec_kick( 50 , 35  )
            return 
        

        self.swingNeck() 

        self.exec_dash( 100 )

        self.__debugTick += 1 
        

    def swingNeck( self ) :       
        angle = math.sin( math.pi/2.0 * self.observer.time ) * 90
        self.exec_turnNeck( angle) 




    def exec_moveTo( self, x,y ) :
        cmd = getCmdSymbol( 'move' )
        s = writelisp( ( cmd , x, y   )  )
        # if True: return 
        self.sendMsg( s )

    def exec_turnNeck( self, angle  ) :
        cmd = getCmdSymbol( 'turn_neck' )  
        s = writelisp( ( cmd , angle  )  )
        self.sendMsg( s ) 

    def exec_dash( self, power) :
        cmd = getCmdSymbol( 'dash' )  
        s = writelisp( ( cmd , power  )  )
        self.sendMsg( s ) 
        
    def exec_kick( self, power , angle ) :   
        cmd = getCmdSymbol( 'kick' )  
        s = writelisp( ( cmd , power , angle  )  )
        self.sendMsg( s ) 
        

