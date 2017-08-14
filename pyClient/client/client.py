from parser import Parser
from serverparam import ServerParam 
from playerparam import PlayerParam 
from rcss import PM_BeforeKickOff  , PM_PlayOn , PM_KickOff_Left
from readlisp import writelisp ,  getCmdSymbol
import random  
import math 
from utility import *
from worldstate import WorldState 
from euclid import Vector2
from rcss import *

class Client(Parser) :
    def __init__( self, send2server , teamname):
        super( Client , self ).__init__() 
        self.__send2server = send2server 
        self.__teamname = teamname 
        self.__debugTick = 0

    def sendMsg( self, msg ) :
        self.__send2server( msg + '\0' )


    def SendInitialLizeMsg(self) :
        helloMsg = b"(init {0} (version 15))".format( self.__teamname ) 
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

    def plan(self):
        try:
            self.plan2()
        except:
            import traceback
            traceback.print_exc()
            print err

    def plan2( self ) :
        if not self.observer.initialized:
            return 

        # update world state before do decision
        if not WorldState.instance().update( self.observer ):
            return 


        if self.observer.serverPlayMode == PM_BeforeKickOff  : 
            x = random.uniform( -ServerParam.instance().PITCH_LENGTH/2.0 , 0 ) 
            y = random.uniform( -ServerParam.instance().PITCH_WIDTH/2.0 , ServerParam.instance().PITCH_WIDTH/2.0 ) 
            if self.observer.needRotate:
                x *= -1
            self.exec_moveTo( x,y )
            return 
        # if self.observer.serverPlayMode == PM_PlayOn:
        #     self.planScore()
        self.planScore()

        self.swingNeck() 
        self.__debugTick += 1 
        
    def planScore(self) :
        selfAgent = WorldState.instance().selfAgent  
        ball = WorldState.instance().ball 

        relAngle2ball = selfAgent.relAngle2Point( ball.position )
        
        if selfAgent.ballKickable():
            oppGoal = self.getOppGoal()
            relAngle2OppGoal = selfAgent.relAngle2Point( oppGoal.marker_position )
            self.exec_kick( ServerParam.instance().maxPower() , relAngle2OppGoal )
        elif abs(relAngle2ball) < 15 :
            # print ServerParam.instance().maxPower() , ServerParam.instance().minPower()
            vec2ball = ball.position - selfAgent.position 
            self.exec_dash( min( ServerParam.instance().maxPower() , vec2ball.magnitude() * 20   ) ) 
        else :
            self.exec_turn( relAngle2ball )



        pass  

    def swingNeck( self ) :       
        angs = ( -90, 90, 90 ,-90 )
        angle = angs[ self.__debugTick % len( angs ) ]
        self.exec_turnNeck( angle) 


    def sendCmd( self,cmd ):
        s = writelisp( cmd  )
        self.sendMsg( s )
        WorldState.instance().recordActionCmd( str(cmd[0]) , cmd[1:] )

    def exec_moveTo( self, x,y ) :
        cmd = getCmdSymbol( 'move' )
        self.sendCmd( ( cmd , x, y   )  )

    def exec_turnNeck( self, angle  ) :
        cmd = getCmdSymbol( 'turn_neck' )  
        self.sendCmd( ( cmd , normalize_angle( angle )  )  )

    def exec_dash( self, power) :
        cmd = getCmdSymbol( 'dash' )  
        self.sendCmd( ( cmd , power  )  )
        
    def exec_kick( self, power , angle ) :   
        cmd = getCmdSymbol( 'kick' )  
        self.sendCmd( ( cmd , power , normalize_angle( angle )  )  )

    def exec_turn( self , angle  ):
        cmd = getCmdSymbol( 'turn' )  
        self.sendCmd( ( cmd , normalize_angle( angle )   )  )


    # ========= desision =================
    def getOppGoal(self):
        return self.observer.mMarkerObservers[Goal_R ] if not self.observer.needRotate  else self.observer .mMarkerObservers[Goal_L ]
