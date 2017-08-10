from serverparam import ServerParam 
from rcss import PM_BeforeKickOff , PM_PlayOn 
from rc_types import *
from utils import cUnDelete 

class ObserverRecord(cUnDelete) :
    __slots__ = { "time" , "value" }
    def __init__(self) :
        super( ObserverRecord , self ).__init__()
        self.time = -1
        self.value = 0
    def update( self, time, value  ) :
        self.time = time 
        self.value = value 

class GameObject( cUnDelete ) :
    __slots__ = { "distance" , "direction" }  
    def __init__( self ) :
        super(GameObject,self ).__init__()
        self.distance = ObserverRecord()
        self.direction = ObserverRecord()
    def __getitem__(self, key) :
        return getattr( self, key  )
    # def __setitem__(self,key, value) :
    #     print "set like dict"

class Line( GameObject ) :  # ====================================
    __slots__ = ()

class FieldObject( GameObject ) :
    __slots__ = { "position" } 
    def __init__(self) :
        super( FieldObject , self ).__init__()
        self.position = ObserverRecord()  

class Marker( FieldObject ) :    # ====================================   
    # must explictly define __slots__ even if it is empty
    __slots__ = {}

class MobileObject( FieldObject ) :
    __slots__ = { "direction_change" , "distance_change" , "speed_vector" } 
    def __init__(self) :
        super( MobileObject, self ).__init__() 
        self.direction_change = ObserverRecord()
        self.distance_change = ObserverRecord()
        self.speed_vector = ObserverRecord()

class Ball( MobileObject ) :   # ====================================  
    __slots__ = {} 

    def update(self, time , prop):
        for k,v in prop.iteritems():
            self[k].update( time, v  )

class Player( MobileObject ) :   # ====================================  
    __slots__ = {"team","side","unum", "body_direction" , "face_direction" , "neck_direction" } 
    def __init__(self) :
        super( Player, self ).__init__() 
        self.team = ""
        self.side = "?"
        self.unum = -1 
        self.body_direction = ObserverRecord()
        self.face_direction = ObserverRecord()
        self.neck_direction = ObserverRecord()



         

class Observer(cUnDelete):
    __slots__ = { "initialized" , "__initSide" , "side" , "unum" , "serverPlayMode" , "needRotate" , 
        "__time" , "__sight_time" , "__sense_body_time" , "__bodyInfo", "__bodyFutureInfo" , 
        "ballObserver" , "mLineObservers" , "mMarkerObservers" , 
        }
    
    def __init__(self) :
        super(Observer,self).__init__()
        self.initialized = False 
        self.__initSide = None 
        self.side = None 
        self.unum = None
        self.serverPlayMode = None 

        self.needRotate = False 

        self.__time = -1
        self.__sight_time = -1
        self.__sense_body_time = -1

        self.ballObserver = Ball() 
        self.mLineObservers = tuple( [ Line() for i in xrange(SL_MAX) ]  )  
        self.mMarkerObservers =  tuple( [ Marker() for i in xrange(FLAG_MAX ) ]  )  

        self.__bodyInfo = {}
        self.__bodyFutureInfo = []

    # handel init msg
    def init(self, my_side , my_unum , play_mode ):
        self.__initSide = my_side 
        self.side = my_side 
        self.unum = my_unum

        if play_mode == PM_BeforeKickOff :
            self.serverPlayMode = play_mode
            self.playMode = play_mode 

            self.kickoffMode = KO_Ours if self.__initSide == 'r' else KO_Opps 
        else:
            self.serverPlayMode = PM_PlayOn 
            self.serverPlayMode = PM_PlayOn 

    def update( self, time , *prop ):
        self.__time = time 
        # print "sense body" , time 

    @property 
    def sight_time( self ):
        return self.__sight_time 
    
    @sight_time.setter
    def sight_time(self, value):
        self.__sight_time = value 
        self.updateWorldStateTime()

        self.__syncBodyInfo2WorldState()  

    @property 
    def sense_body_time( self ):
        return self.__sense_body_time
    
    @sense_body_time.setter
    def sense_body_time(self, value):
        self.__sense_body_time = value 


    @property
    def worldstate_time(self) :
        return self.__time

    def updateWorldStateTime(self):
        self.__time = max( self.__sight_time , self.__time   )

    @property
    def initSide(self) :
        return __initSide 

    def recordBodyInfo(self, d) :
        from copy import deepcopy 
        dup = deepcopy(d) 
        self.__bodyFutureInfo.insert( 0, dup )

        self.__syncBodyInfo2WorldState()  

    def __syncBodyInfo2WorldState(self) :
        while len( self.__bodyFutureInfo ) > 0:
            info =  self.__bodyFutureInfo[-1]
            if info["time"] <= self.__time:
                self.__bodyInfo.update( info ) 
                self.__bodyFutureInfo.pop()
            else:
                break 


    # body infos
    @property
    def agentBodyDirection( self ):
        return self.__bodyInfo[ "speed_dir" ] + self.__bodyInfo[ "head_angle" ]   
    @property
    def agentHeadDirection( self ):
        return self.__bodyInfo[ "head_angle" ]


    def Initialize(self) :
        assert self.side is not None

        # if true, multiply all coords by -1 inside initialize
        self.needRotate  = False if self.side == 'r' else True 
        self.InitializeFlags( self.needRotate  ) 
        self.initialized = True 

    def InitializeFlags(self, rotation ) :
        pass 

