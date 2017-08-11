
from utils import Singleton , cUnDelete
from utility import *
from rc_types import *
import operator
import math
from euclid import Vector2

class WorldObject( cUnDelete) :
    __slots__ = { "bodyDirection" , "headDirection" , "position" }
    def __init__(self):
        super( WorldObject , self ).__init__()
        self.bodyDirection = 0
        self.headDirection = 0
        self.__position = Vector2( -1, -1 )

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value) :
        if isinstance(value, Vector2):
            self.__position.x = float(value.x) 
            self.__position.y = float(value.y) 
        else:
            self.__position.x = float(value[0]) 
            self.__position.y = float(value[1]) 
        

class WorldState( cUnDelete ):
    __metaclass__ = Singleton
    
    def __init__(self):
        super( WorldState , self ).__init__()
        self.serverWorldStateTime = -1  # the latest server time 
        # don't use timeUpdated to do anything
        self.timeUpdated = -1  # the time agent last updated


        self.ball = WorldObject() 
        self.teamPlayers = tuple( [ WorldObject() for i in xrange(11) ]  ) 
        self.oppPlayers = tuple( [ WorldObject() for i in xrange(11) ]  ) 
        
        # must sync with observer's mobleObserver
        self.mobileObjects = [ self.ball ]

        

    @classmethod
    def instance(cls):
        return WorldState() 

    @property
    def selfAgent(self) :
        return self.teamPlayers[ self.__observer.unum ]

    def updateServerWorldStateTime( self, time ) :
        self.serverWorldStateTime = max( self.serverWorldStateTime , time  )

    def updateSelfAgent(self, observer , time ):
        selfAgent = self.selfAgent  
        bodyInfo = observer.bodyFutureInfo[time]

        lines = [ line for line in observer.mLineObservers if line.direction.time == time and line.distance.time == time ]
        if len( lines ) == 0:
            # print "no line for locating found" , time 
            return False 
        line = min( lines , key=operator.attrgetter( "distance.value"  )  ) 

        markers = [marker for marker in observer.mMarkerObservers if marker.direction.time == time and marker.distance.time == time and marker.distance.value > 2 ]
        if len(markers) == 0:
            # print "no marker for locating found" , time 
            return False 
        marker = min( markers , key=operator.attrgetter( "distance.value"  )  ) 

        alpha = line.direction.value
        beta = -math.copysign( 1.0,alpha ) * ( 90 - abs(alpha) )

        line_global_angles = ( -180,0,-90,90 )
        global_head_dir = line_global_angles[ line.field_type  ] - beta 
        theta = global_head_dir
        global_body_dir = global_head_dir - bodyInfo[ "head_angle" ]

        selfAgent.bodyDirection = global_body_dir 
        selfAgent.headDirection = theta 

        # =======
        rpos = fromPolar( marker.distance.value , marker.direction.value + theta  )
        # print id( selfAgent.position ) , "~~~"
        selfAgent.position = marker.marker_position - rpos
        # print id( selfAgent.position  )


        del observer.bodyFutureInfo[time]   


        if False :
            print "marker:" , marker.marker_position.value  , markerType2str( marker.field_type )
            print "body dir :" ,  selfAgent.bodyDirection , "pos" , selfAgent.position , "dis:" ,  marker.distance.value , "dir:" , marker.direction.value 
        

        self.timeUpdated = time
        return True  

    def updateOtherMobileObject( self , observer , time ):
        selfAgent = self.selfAgent  
        theta = selfAgent.headDirection
        
        objs = [(i,obj) for i,obj in enumerate( self.mobileObjects ) if obj is not selfAgent and observer.mobileObservers[i].direction.time == time and observer.mobileObservers[i].distance.time == time ]
        for i, obj in objs:
            objObserver = observer.mobileObservers[i]
            rpos = fromPolar( objObserver.distance.value , objObserver.direction.value + theta )
            obj.position = selfAgent.position + rpos

            # print obj.position 
            if hasattr( objObserver, "body_direction" ) and objObserver.body_direction.time == time:
                obj.bodyDirection = objObserver.body_direction.value + theta  

            if hasattr( objObserver, "neck_direction" ) and objObserver.neck_direction.tiem == time :
                obj.headDirection = objObserver.neck_direction.value + theta 

            

        pass

    def update(self , observer ):
        self.__observer = observer 
        
        # print "last up t:{0},serv t:{1}, sight t:{2} , body t:{3}".format( self.timeUpdated ,self.serverWorldStateTime, observer.lastest_sight_time , observer.lastest_sensebody_time)
        if observer.lastest_sight_time < 0 or len( observer.bodyFutureInfo ) == 0 :
            return False 

        # remove expired body info 
        if len( observer.bodyFutureInfo ) > 10:
            keys = observer.bodyFutureInfo.keys()
            keys.sort()
            nkey2remove = len( observer.bodyFutureInfo ) - 10 
            for i in xrange( nkey2remove ) :
                del observer.bodyFutureInfo[ keys[0]] 

        if observer.lastest_sight_time <= observer.lastest_sensebody_time :
            time2update = observer.lastest_sight_time
            if time2update in observer.bodyFutureInfo:
                # update 
                if self.updateSelfAgent(observer , time2update  ) :
                    # update other mobile object
                    self.updateOtherMobileObject( observer , time2update  )

            return True
        else:
            print "warning: short of sensebody time " 
            return False 



