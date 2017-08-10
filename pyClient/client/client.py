from parser import Parser
from serverparam import ServerParam 
from playerparam import PlayerParam 
from rcss import PM_BeforeKickOff  , PM_PlayOn , PM_KickOff_Left
from readlisp import writelisp ,  getCmdSymbol
import random  
import math 
from utility import *
from worldstate import WorldState 

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

        # update world state before do decision
        WorldState.instance().update( self.observer )


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

        # self.exec_dash( 100 )

        try:
            # self.planScore()
            pass
        except Exception as err:
            print err

        self.__debugTick += 1 
        
    def planScore(self) :
        
        bodyDir = self.observer.agentGlobalBodyDirection
        if bodyDir is not None:
            ballRelDir = self.observer.ballObserver.direction.value 
            headDir = self.observer.agentHeadDirection 
            dir2ball = normalize_angle(  headDir + ballRelDir - bodyDir )
            
            if bodyDir != 0:
                print "aaaa", bodyDir , ballRelDir , headDir , dir2ball 

            if abs( dir2ball ) > 2 :
                # self.exec_turn( dir2ball ) 
                return
            else :
                pass 
                # exec_dash( ServerParam.instance().maxpower()  )

        

        pass  

    def swingNeck( self ) :       
        angs = ( -90, 90, 90 ,-90 )
        angle = angs[ self.__debugTick % len( angs ) ]
        self.exec_turnNeck( angle) 




    def exec_moveTo( self, x,y ) :
        cmd = getCmdSymbol( 'move' )
        s = writelisp( ( cmd , x, y   )  )
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

    def exec_turn( self , angle  ):
        cmd = getCmdSymbol( 'turn' )  
        s = writelisp( ( cmd , angle  )  )
        self.sendMsg( s ) 

        

