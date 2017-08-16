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
        self.observer.teamname = teamname 
        self.__debugTick = 0

    def sendMsg( self, msg ) :
        self.__send2server( msg + '\0' )


    def SendInitialLizeMsg(self) :
        helloMsg = b"(init {0} (version 15))".format( self.observer.teamname ) 
        self.sendMsg( helloMsg  )
        

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


        # self.planScore()
        # self.planPassing()
        self.planBallFacing()

        self.__debugTick += 1 

    def planBallFacing(self):
        if self.observer.serverPlayMode == PM_BeforeKickOff and not self.observer.bDoneInState : 
            x = random.uniform( -ServerParam.instance().PITCH_LENGTH/2.0 , 0 ) 
            y = random.uniform( -ServerParam.instance().PITCH_WIDTH/2.0 , ServerParam.instance().PITCH_WIDTH/2.0 ) 
            if self.observer.needRotate:
                x *= -1
            self.exec_moveTo( x,y )

            self.observer.bDoneInState = True
            return 

        ball = WorldState.instance().ball 

        if not ball.sawInLastSight():
            self.searching()
        else:
            self.turnTo( ball.position )
            # self.swingNeck()

            if ball.sawInLastestServerTime():
                # print 'say' ,  WorldState.instance().serverWorldStateTime 
                self.exec_say( " ".join( map(str, ( 'b',0,int(ball.position.x),int(ball.position.y) ) ) ) ) 
            

        pass

    def planPassing(self):
        if self.observer.serverPlayMode == PM_BeforeKickOff and not self.observer.bDoneInState : 
            x = random.uniform( -ServerParam.instance().PITCH_LENGTH/2.0 , 0 ) 
            y = random.uniform( -ServerParam.instance().PITCH_WIDTH/2.0 , ServerParam.instance().PITCH_WIDTH/2.0 ) 
            if self.observer.needRotate:
                x *= -1
            self.exec_moveTo( x,y )

            self.observer.bDoneInState = True
            return 

        selfAgent = WorldState.instance().selfAgent
        ball = WorldState.instance().activeBall()
        mate = WorldState.instance().anyPlayer()

        if ball is None :
            self.searching()
            return 

        if selfAgent.ballKickable():
            if mate is None:
                self.searching()
            else:
                relAng = selfAgent.relAngle2Point( mate.position ) 
                self.exec_kick( ServerParam.instance().maxPower() , relAng )
        elif ball.velocity.magnitude_squared() < 0.25 : 
            if mate is None:
                self.searching()
            elif selfAgent.position.distance2( ball.position ) <  mate.position.distance2( ball.position ) :
                self.runTo( ball.position ) 
            else:
                self.searching()
        else:
            self.swingNeck() 

        
    def planScore(self) :
        if self.observer.serverPlayMode == PM_BeforeKickOff and not self.observer.bDoneInState : 
            x = random.uniform( -ServerParam.instance().PITCH_LENGTH/2.0 , 0 ) 
            y = random.uniform( -ServerParam.instance().PITCH_WIDTH/2.0 , ServerParam.instance().PITCH_WIDTH/2.0 ) 
            if self.observer.needRotate:
                x *= -1
            self.exec_moveTo( x,y )

            self.observer.bDoneInState = True
            return 

        selfAgent = WorldState.instance().selfAgent  
        ball = WorldState.instance().ball 

        relAngle2ball = selfAgent.relAngle2Point( ball.position )
        
        if ball.isSightExpired():
            self.searching()
        
        elif selfAgent.ballKickable():
            oppGoal = self.getOppGoal()
            relAngle2OppGoal = selfAgent.relAngle2Point( oppGoal.marker_position )
            self.exec_kick( ServerParam.instance().maxPower() , relAngle2OppGoal )
        elif abs(relAngle2ball) < 15 :
            # print ServerParam.instance().maxPower() , ServerParam.instance().minPower()
            vec2ball = ball.position - selfAgent.position 
            self.exec_dash( min( ServerParam.instance().maxPower() , vec2ball.magnitude() * 20   ) ) 
        else :
            self.exec_turn( relAngle2ball )

        self.swingNeck() 


    def searching(self):
        # from observer import Observer
        # print WorldState.instance().serverWorldStateTime ,  Observer.instance().lastest_sight_time 
        if WorldState.instance().lastestSightInfoArrived():
            # print "turning " , WorldState.instance().serverWorldStateTime  
            self.exec_turn( 90 )
        self.resetHeadAngle()
        pass  
    
    def runTo( self, pos  ):
        selfAgent = WorldState.instance().selfAgent
        relAng = selfAgent.relAngle2Point( pos )
        if abs(relAng) < 15:
            vec = pos - selfAgent.position 
            self.exec_dash( min( ServerParam.instance().maxPower() , vec.magnitude() * 20   ) ) 
        else:
            self.exec_turn( relAng )

    def turnTo( self, pos ) :
        selfAgent = WorldState.instance().selfAgent
        relAng = selfAgent.relAngle2Point( pos ) 
        self.exec_turn( relAng ) 



    def swingNeck( self ) :       
        angs = ( -90, 90, 90 ,-90 )
        angle = angs[ self.__debugTick % len( angs ) ] / 3 
        self.exec_turnNeck( angle) 

    def resetHeadAngle(self):
        bodyInfo = self.observer.lastest_bodyInfo() 
        self.exec_turnNeck( -bodyInfo[ "head_angle" ] ) 

    def writeSendMsg( self,cmd ):
        s = writelisp( cmd  )
        self.sendMsg( s )
        WorldState.instance().recordActionCmd( str(cmd[0]) , cmd[1:] )

    def exec_moveTo( self, x,y ) :
        cmd = getCmdSymbol( 'move' )
        self.writeSendMsg( ( cmd , x, y   )  )

    def exec_turnNeck( self, angle  ) :
        cmd = getCmdSymbol( 'turn_neck' )  
        self.writeSendMsg( ( cmd , normalize_angle( angle )  )  )

    def exec_dash( self, power) :
        cmd = getCmdSymbol( 'dash' )  
        self.writeSendMsg( ( cmd , power  )  )
        
    def exec_kick( self, power , angle ) :   
        cmd = getCmdSymbol( 'kick' )  
        self.writeSendMsg( ( cmd , power , normalize_angle( angle )  )  )

    def exec_turn( self , angle  ):
        cmd = getCmdSymbol( 'turn' )  
        self.writeSendMsg( ( cmd , normalize_angle( angle )   )  )

    def exec_say( self , msg  ):
        cmd = getCmdSymbol( 'say' )
        self.writeSendMsg(  ( cmd, msg ) )


    # ========= desision =================
    def getOppGoal(self):
        return self.observer.mMarkerObservers[Goal_R ] if not self.observer.needRotate  else self.observer .mMarkerObservers[Goal_L ]

        
