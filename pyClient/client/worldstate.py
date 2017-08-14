
from utils import Singleton , cUnDelete
from utility import *
from rc_types import *
import operator
import math
from euclid import Vector2
from collections import defaultdict
from serverparam import ServerParam
from observer import Observer 

class WorldObject( cUnDelete) :
    def __init__(self, obj_observer ):
        super( WorldObject , self ).__init__()
        self.bodyDirection = 0
        self.neckDirection = 0
        self.__position = Vector2( -1, -1 )
        self.__velocity = Vector2( 0,0 )
        self.obj_observer = obj_observer

    @property
    def position(self):
        return self.__position

    # setter will not assign with new instance ,  copying content instead
    @position.setter
    def position(self, value):
        if isinstance(value, Vector2):
            self.__position.x = float(value.x) 
            self.__position.y = float(value.y) 
        else:
            self.__position.x = float(value[0]) 
            self.__position.y = float(value[1]) 

    @property
    def velocity(self):
        return self.__velocity 

    @velocity.setter
    def velocity(self, value):
        if isinstance(value, Vector2):
            self.__velocity.x = float(value.x) 
            self.__velocity.y = float(value.y) 
        else:
            self.__velocity.x = float(value[0]) 
            self.__velocity.y = float(value[1]) 

class WorldPlayer( WorldObject ) :
    def __init__(self, obj_observer ):
        super( WorldPlayer, self ).__init__( obj_observer )
        # initial setter !
        self.player_type = 0 

    @property
    def player_type(self):
        return self.__player_type 

    @player_type.setter
    def player_type(self, t): 
        self.__player_type = t 
        self.M_player_type = ServerParam.instance().playerTypes[ self.__player_type ] 
    
    def relAngle2Point( self, targetPos ) :
        vecBody = fromPolar_degree( 1.0 , self.bodyDirection )
        vec2target = targetPos - self.position 
        rad2Turn2ball = vecBody.signed_angle_to( vec2target ) 
        angle =  math.degrees ( rad2Turn2ball )
        return angle
    
    def kickableArea(self):
        return self.M_player_type.player_size + ServerParam.instance().ballSize() + self.M_player_type.kickable_margin
                                    
    def ballKickable(self):
        ball = WorldState.instance().ball
        return self.position.distance2( ball.position)  <=  ( self.kickableArea() ** 2 )


class WorldState( cUnDelete ):
    __metaclass__ = Singleton
    
    def __init__(self):
        super( WorldState , self ).__init__()
        self.serverWorldStateTime = -1  # the latest server time 
        # don't use timeUpdated to do anything
        self.timeUpdated = -1  # the time agent last updated

        self.ball = WorldObject( Observer.instance().ballObserver  ) 
        self.teamPlayers = tuple( [ WorldPlayer( Observer.instance().mSelfPlayerObservers[i] ) for i in xrange(11) ]  ) 
        self.oppPlayers =  tuple( [ WorldPlayer( Observer.instance().mOppPlayerObservers[i]  ) for i in xrange(11) ]  ) 
        
        # must sync with observer's mobleObserver
        self.mobileObjects = [ self.ball ]

        self.__actionCmdHistory = defaultdict( dict )
        

    @classmethod
    def instance(cls):
        return WorldState() 

    @property
    def selfAgent(self) :
        return self.teamPlayers[ Observer.instance().unum-1 ]

    def updateServerWorldStateTime( self, time ) :
        self.serverWorldStateTime = max( self.serverWorldStateTime , time  )

    def updateSelfAgent(self, observer , time ):
        selfAgent = self.selfAgent  
        bodyInfo = observer.bodyFutureInfo[time]

        # rule 1: use nearest line
        lines = [ line for line in observer.mLineObservers if line.direction.time == time and line.distance.time == time ]
        if len( lines ) == 0:
            # print "no line for locating found" , time 
            return False 
        line = min( lines , key=operator.attrgetter( "distance.value"  )  ) 

        markers = [marker for marker in observer.mMarkerObservers if marker.direction.time == time and marker.distance.time == time and marker.distance.value > 0.5 ]
        if len(markers) == 0:
            # print "no marker for locating found" , time 
            return False 
        marker = min( markers , key=operator.attrgetter( "distance.value"  )  ) 

        alpha = line.direction.value
        beta = -math.copysign( 1.0,alpha ) * ( 90 - abs(alpha) )

        global_head_dir = math.degrees(  Vector2(1,0).signed_angle_to( line.marker_position ))  - beta 
        # rule 2: if agent see 2 lines , it means he is outside the pitch
        if len(lines) >= 2:
            global_head_dir += 180
        global_head_dir = normalize_angle( global_head_dir )
        theta = global_head_dir

        global_body_dir = normalize_angle(  global_head_dir - bodyInfo[ "head_angle" ] )

        selfAgent.bodyDirection = global_body_dir 
        selfAgent.neckDirection = theta 

        # =======
        rpos = fromPolar_degree( marker.distance.value , marker.direction.value + theta  )
        # print id( selfAgent.position ) , "~~~"
        selfAgent.position = marker.marker_position - rpos
        # print id( selfAgent.position  )


        # === update self velocity ================
        self.velocity = fromPolar_degree( bodyInfo[ "speed" ] , bodyInfo[ "speed_dir"] + theta  )


        # keep , do not delete
        # del observer.bodyFutureInfo[time]   


        if False :
            print "marker:" , marker.marker_position.value  , markerType2str( marker.field_type )
            print "body dir :" ,  selfAgent.bodyDirection , "pos" , selfAgent.position , "dis:" ,  marker.distance.value , "dir:" , marker.direction.value 
        

        self.timeUpdated = time
        return True  

    def updateOtherMobileObject( self , observer , time ):
        selfAgent = self.selfAgent  
        theta = selfAgent.neckDirection
        
        objs = [(i,obj) for i,obj in enumerate( self.mobileObjects ) if obj is not selfAgent and observer.mobileObservers[i].direction.time == time and observer.mobileObservers[i].distance.time == time ]
        for i, obj in objs:
            objObserver = observer.mobileObservers[i]
            rpos = fromPolar_degree( objObserver.distance.value , objObserver.direction.value + theta )
            obj.position = selfAgent.position + rpos

            # print obj.position 
            if hasattr( objObserver, "body_direction" ) and objObserver.body_direction.time == time:
                obj.bodyDirection = objObserver.body_direction.value + theta  

            if hasattr( objObserver, "neck_direction" ) and objObserver.neck_direction.time == time :
                obj.neckDirection = objObserver.neck_direction.value + theta 
            
            if hasattr( objObserver, "distance_change" ) and objObserver.distance_change.time == time and \
                    hasattr( objObserver, "direction_change" ) and objObserver.direction_change.time == time :

                # calc velocity
                distChg = objObserver.distance_change.value 
                dirChg = objObserver.direction_change.value 
                objDist = objObserver.distance.value 
                objDir = objObserver.direction.value

                relPos = fromPolar_degree(1.0,  objDir ) 

                relVel = Vector2(distChg*relPos.x - (dirChg*math.pi/180*objDist * relPos.y) ,
                                 distChg*relPos.y + (dirChg*math.pi/180*objDist * relPos.x)  )
                obj.velocity = selfAgent.velocity +  relVel.rotate( math.radians( selfAgent.neckDirection ) )

                # print "obj vel:",  obj.velocity 


            

        pass

    def predictionSelfAgent( self, observer ):
        for time in xrange( self.timeUpdated , observer.lastest_sensebody_time ):
            if time in observer.bodyFutureInfo and time+1 in observer.bodyFutureInfo :
                bodyInfo_t = observer.bodyFutureInfo[time]
                bodyInfo_tp1 = observer.bodyFutureInfo[time+1]

                diff = { k:v-bodyInfo_t[k]  for k,v in bodyInfo_tp1.iteritems() if isinstance( v, int ) }


                
            else:
                # print 'can not prediction, short of body info histroy' , self.timeUpdated , observer.lastest_sensebody_time 
                break 
        

    def update(self , observer ):
        
        # print "last up t:{0},serv t:{1}, sight t:{2} , body t:{3}".format( self.timeUpdated ,self.serverWorldStateTime, observer.lastest_sight_time , observer.lastest_sensebody_time)
        # does not start yet , or no body sense info
        if observer.lastest_sight_time < 0 or len( observer.bodyFutureInfo ) == 0 :
            return False 

        # remove expired body info 
        if len( observer.bodyFutureInfo ) > 10:
            keys = observer.bodyFutureInfo.keys()
            keys.sort()
            nkey2remove = len( observer.bodyFutureInfo ) - 10 
            for i in xrange( nkey2remove ) :
                del observer.bodyFutureInfo[ keys[i]] 

        if observer.lastest_sight_time <= observer.lastest_sensebody_time :
            time2update = observer.lastest_sight_time
            if time2update in observer.bodyFutureInfo:
                # update 
                if self.updateSelfAgent(observer , time2update  ) :
                    # update other mobile object
                    self.updateOtherMobileObject( observer , time2update  )
        else:
            print "warning: short of sensebody time " 

        self.predictionSelfAgent( observer ) 

        return True

    def recordActionCmd(self, cmd, param ):
        if cmd not in self.__actionCmdHistory[ self.serverWorldStateTime ]: 
            self.__actionCmdHistory[ self.serverWorldStateTime ][cmd] = param 


