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
            x = random.uniform( 0, ServerParam.instance().PITCH_LENGTH/2.0 ) 
            y = random.uniform( -ServerParam.instance().PITCH_WIDTH/2.0 , ServerParam.instance().PITCH_WIDTH/2.0 ) 
            if self.observer.needRotate:
                x *= -1
            self.exec_moveTo( x,y )
            return 
        # if self.observer.serverPlayMode == PM_KickOff_Left :
        #     self.exec_kick( 50 , 35  )
        #     return 
        #
        # if self.observer.serverPlayMode == PM_PlayOn:
        #     self.planScore()
        self.planScore()

        self.swingNeck() 
        self.__debugTick += 1 
        
    def planScore(self) :
        selfAgent = WorldState.instance().selfAgent  
        ball = WorldState.instance().ball 

        relAngle2ball = self.relAngle2Point( ball.position )
        if self.observer.needRotate:
            print selfAgent.position

        if self.ballKickable():
            relAngle2OppGoal = self.relAngle2Point( self.observer.mMarkerObservers[Goal_R ].marker_position )
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




    def exec_moveTo( self, x,y ) :
        cmd = getCmdSymbol( 'move' )
        s = writelisp( ( cmd , x, y   )  )
        self.sendMsg( s )

    def exec_turnNeck( self, angle  ) :
        cmd = getCmdSymbol( 'turn_neck' )  
        s = writelisp( ( cmd , normalize_angle( angle )  )  )
        self.sendMsg( s ) 

    def exec_dash( self, power) :
        cmd = getCmdSymbol( 'dash' )  
        s = writelisp( ( cmd , power  )  )
        self.sendMsg( s ) 
        
    def exec_kick( self, power , angle ) :   
        cmd = getCmdSymbol( 'kick' )  
        s = writelisp( ( cmd , power , normalize_angle( angle )  )  )
        self.sendMsg( s ) 

    def exec_turn( self , angle  ):
        cmd = getCmdSymbol( 'turn' )  
        s = writelisp( ( cmd , normalize_angle( angle )   )  )
        self.sendMsg( s ) 

    # ==  player ================================
    def relAngle2Point( self, targetPos ) :
        selfAgent = WorldState.instance().selfAgent  

        vecBody = fromPolar( 1.0 , selfAgent.bodyDirection )
        vec2target = targetPos - selfAgent.position 
        rad2Turn2ball = vecBody.signed_angle_to( vec2target ) 
        angle =  math.degrees ( rad2Turn2ball )
        return angle
    
    def kickableArea(self):
        M_player_type = ServerParam.instance().playerTypes[ self.observer.playerTypeID  ]
        return M_player_type.player_size + ServerParam.instance().ballSize() + M_player_type.kickable_margin
                                    
    def ballKickable(self):
        ball = WorldState.instance().ball 
        selfAgent = WorldState.instance().selfAgent
        return selfAgent.position.distance2( ball.position)  <=  ( self.kickableArea() ** 2 )

