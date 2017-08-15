from serverparam import ServerParam 
from rcss import PM_BeforeKickOff , PM_PlayOn 
from rc_types import *
from utils import cUnDelete , Singleton 
import sys , math
from utility import *
from euclid import Vector2



class ObserverRecord(cUnDelete) :
    __slots__ = { "time" , "value" }
    def __init__(self) :
        super( ObserverRecord , self ).__init__()
        self.time = -1
        self.value = 0
    def update( self, time, value  ) :
        if time < self.time :
            return 
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

    def update(self, time , prop):
        for k,v in prop.iteritems():
            self[k].update( time, v  )


class FieldObject( GameObject ) :
    __slots__ = { "marker_position" , "direction_change" , "distance_change" , "field_type" } 
    def __init__(self) :
        super( FieldObject , self ).__init__()
        self.marker_position = None
        self.direction_change = ObserverRecord()
        self.distance_change = ObserverRecord()
        self.field_type = -1

    def Initialize( self , field_type, pos , rotation ) :
        # If on the right side of the field, flip all coords
        pos = Vector2( *pos )
        self.marker_position = pos if not rotation else -pos 
        self.field_type = field_type


class Line( FieldObject ) :    # ====================================   
    # must explictly define __slots__ even if it is empty
    __slots__ = {}

class Marker( FieldObject ) :    # ====================================   
    # must explictly define __slots__ even if it is empty
    __slots__ = {}

class MobileObject( FieldObject ) :
    __slots__ = { "speed_vector" } 
    def __init__(self) :
        super( MobileObject, self ).__init__() 
        self.speed_vector = ObserverRecord()

class Ball( MobileObject ) :   # ====================================  
    __slots__ = {} 


class Player( MobileObject ) :   # ====================================  
    __slots__ = {"team","side","unum", "body_direction" , "head_direction" } # "face_direction"  
    def __init__(self) :
        super( Player, self ).__init__() 
        self.team = ""
        self.side = "?"
        self.unum = -1 
        self.body_direction = ObserverRecord()
        # self.face_direction = ObserverRecord()
        self.head_direction = ObserverRecord()



         

class Observer(cUnDelete):
    __metaclass__ = Singleton


    @classmethod
    def instance(cls):
        return Observer() 
    
    def __init__(self) :
        super(Observer,self).__init__()
        self.initialized = False 
        self.__initSide = None 
        self.teamname = ''
        self.side = None 
        self.unum = None

        self.__serverPlayMode = None 
        self.bDoneInState = False

        self.needRotate = False 

        self.__sight_time = -1
        self.__sensebody_time = -1

        self.ballObserver = Ball() 
        self.mLineObservers = tuple( [ Line() for i in xrange(SL_MAX) ]  )  
        self.mMarkerObservers =  tuple( [ Marker() for i in xrange(FLAG_MAX ) ]  )  
        self.mSelfPlayerObservers = tuple( [ Player() for i in xrange(11) ]  ) 
        self.mOppPlayerObservers = tuple( [ Player() for i in xrange(11) ]  ) 

        self.mUnknownPlayerObservers = tuple( [ Player() for i in xrange(11*2) ]  ) 


        self.bodyFutureInfo = {}


    # handel init msg
    def init(self, my_side , my_unum , play_mode ):
        self.__initSide = my_side 
        self.side = my_side 
        self.unum = int(my_unum)

        if play_mode == PM_BeforeKickOff :
            self.serverPlayMode = play_mode

            self.kickoffMode = KO_Ours if self.__initSide == 'r' else KO_Opps 
        else:
            self.serverPlayMode = PM_PlayOn 
            self.serverPlayMode = PM_PlayOn 


    @property
    def serverPlayMode(self):
        return self.__serverPlayMode 

    @serverPlayMode.setter
    def serverPlayMode(self, mode ):
        self.__serverPlayMode = mode
        self.bDoneInState = False 

    @property 
    def lastest_sight_time( self ):
        return self.__sight_time 
    
    @lastest_sight_time.setter
    def lastest_sight_time(self, value):
        self.__sight_time = value 


    @property 
    def lastest_sensebody_time( self ):
        return self.__sensebody_time 
    
    @lastest_sensebody_time.setter
    def lastest_sensebody_time(self, value):
        self.__sensebody_time = value 




    @property
    def initSide(self) :
        return self.__initSide 

    def selfAgentObserver( self ) :
        return self.mSelfPlayerObservers[ self.unum-1 ]

    def recordBodyInfo(self, d) :
        self.bodyFutureInfo[ d["time"] ] = d

    def lastest_bodyInfo(self ):
        return self.bodyFutureInfo[ self.lastest_sensebody_time  ]

    def resetUnknownPlayerObserver(self):
        for obs in self.mUnknownPlayerObservers:
            obs.distance.time = -1

    def updateUnknownPlayerObserver(self ,time, prop ):
        for obs in self.mUnknownPlayerObservers:
            if obs.distance.time == -1:
                obs.update( time , prop )
                break 


    def Initialize(self) :
        assert self.side is not None

        # if true, multiply all coords by -1 inside initialize
        self.needRotate  = False if self.side == 'l' else True 
        self.InitializeFlags( self.needRotate  ) 
        self.initialized = True 

    def InitializeFlags(self, rotation ) :

        pitch_length = ServerParam.instance().PITCH_LENGTH
        pitch_width  = ServerParam.instance().PITCH_WIDTH
        pitch_margin = ServerParam.instance().PITCH_MARGIN
        goal_width   = ServerParam.instance().goalWidth()
        penalty_area_length = ServerParam.instance().PENALTY_AREA_LENGTH
        penalty_area_width  = ServerParam.instance().PENALTY_AREA_WIDTH

        # goals
        self.mMarkerObservers[Goal_L ].Initialize(Goal_L,  ( -pitch_length/2.0, 0.0 ), rotation)  # Goal_L 
        self.mMarkerObservers[Goal_R ].Initialize(Goal_R,  ( pitch_length/2.0, 0.0 ), rotation)  # Goal_R 

        # center
        self.mMarkerObservers[Flag_C ].Initialize(Flag_C,  ( 0.0, 0.0 ), rotation)  # Flag_C 
        self.mMarkerObservers[Flag_CT].Initialize(Flag_CT, ( 0.0, -pitch_width/2.0 ), rotation)  # Flag_CT 
        self.mMarkerObservers[Flag_CB].Initialize(Flag_CB, ( 0.0, pitch_width/2.0 ), rotation)  # Flag_CB 

        # field corner
        self.mMarkerObservers[Flag_LT].Initialize(Flag_LT, ( -pitch_length/2.0, -pitch_width/2.0 ), rotation)  # Flag_LT 
        self.mMarkerObservers[Flag_LB].Initialize(Flag_LB, ( -pitch_length/2.0,  pitch_width/2.0 ), rotation)  # Flag_LB 
        self.mMarkerObservers[Flag_RT].Initialize(Flag_RT, (  pitch_length/2.0, -pitch_width/2.0 ), rotation)  # Flag_RT 
        self.mMarkerObservers[Flag_RB].Initialize(Flag_RB, (  pitch_length/2.0,  pitch_width/2.0 ), rotation)  # Flag_RB 

        # penalty area
        self.mMarkerObservers[Flag_PLT].Initialize(Flag_PLT, ( -pitch_length/2.0+penalty_area_length,-penalty_area_width/2.0 ), rotation)  # Flag_PLT 
        self.mMarkerObservers[Flag_PLC].Initialize(Flag_PLC, ( -pitch_length/2.0+penalty_area_length, 0 ), rotation)  # Flag_PLC 
        self.mMarkerObservers[Flag_PLB].Initialize(Flag_PLB, ( -pitch_length/2.0+penalty_area_length, penalty_area_width/2.0 ), rotation)  # Flag_PLB 
        self.mMarkerObservers[Flag_PRT].Initialize(Flag_PRT, (  pitch_length/2.0-penalty_area_length,-penalty_area_width/2.0 ), rotation)  # Flag_PRT 
        self.mMarkerObservers[Flag_PRC].Initialize(Flag_PRC, (  pitch_length/2.0-penalty_area_length, 0 ), rotation)  # Flag_PRC 
        self.mMarkerObservers[Flag_PRB].Initialize(Flag_PRB, (  pitch_length/2.0-penalty_area_length, penalty_area_width/2.0 ), rotation)  # Flag_PRB 

        # goal area
        self.mMarkerObservers[Flag_GLT].Initialize(Flag_GLT, ( -pitch_length/2.0, -goal_width/2.0 ), rotation)  # Flag_GLT 
        self.mMarkerObservers[Flag_GLB].Initialize(Flag_GLB, ( -pitch_length/2.0,  goal_width/2.0 ), rotation)  # Flag_GLB 
        self.mMarkerObservers[Flag_GRT].Initialize(Flag_GRT, (  pitch_length/2.0, -goal_width/2.0 ), rotation)  # Flag_GRT 
        self.mMarkerObservers[Flag_GRB].Initialize(Flag_GRB, (  pitch_length/2.0,  goal_width/2.0 ), rotation)  # Flag_GRB 

        # top field flags
        self.mMarkerObservers[Flag_TL50].Initialize(Flag_TL50, ( -50.0, -pitch_width/2.0-pitch_margin ), rotation)  # Flag_TL50 
        self.mMarkerObservers[Flag_TL40].Initialize(Flag_TL40, ( -40.0, -pitch_width/2.0-pitch_margin ), rotation)  # Flag_TL40 
        self.mMarkerObservers[Flag_TL30].Initialize(Flag_TL30, ( -30.0, -pitch_width/2.0-pitch_margin ), rotation)  # Flag_TL30 
        self.mMarkerObservers[Flag_TL20].Initialize(Flag_TL20, ( -20.0, -pitch_width/2.0-pitch_margin ), rotation)  # Flag_TL20 
        self.mMarkerObservers[Flag_TL10].Initialize(Flag_TL10, ( -10.0, -pitch_width/2.0-pitch_margin ), rotation)  # Flag_TL10 
        self.mMarkerObservers[Flag_T0  ].Initialize(Flag_T0  , (   0.0, -pitch_width/2.0-pitch_margin ), rotation)  # Flag_T0   
        self.mMarkerObservers[Flag_TR10].Initialize(Flag_TR10, (  10.0, -pitch_width/2.0-pitch_margin ), rotation)  # Flag_TR10 
        self.mMarkerObservers[Flag_TR20].Initialize(Flag_TR20, (  20.0, -pitch_width/2.0-pitch_margin ), rotation)  # Flag_TR20 
        self.mMarkerObservers[Flag_TR30].Initialize(Flag_TR30, (  30.0, -pitch_width/2.0-pitch_margin ), rotation)  # Flag_TR30 
        self.mMarkerObservers[Flag_TR40].Initialize(Flag_TR40, (  40.0, -pitch_width/2.0-pitch_margin ), rotation)  # Flag_TR40 
        self.mMarkerObservers[Flag_TR50].Initialize(Flag_TR50, (  50.0, -pitch_width/2.0-pitch_margin ), rotation)  # Flag_TR50 

        # bottom field flags
        self.mMarkerObservers[Flag_BL50].Initialize(Flag_BL50, ( -50.0, pitch_width/2.0+pitch_margin ), rotation)  # Flag_BL50 
        self.mMarkerObservers[Flag_BL40].Initialize(Flag_BL40, ( -40.0, pitch_width/2.0+pitch_margin ), rotation)  # Flag_BL40 
        self.mMarkerObservers[Flag_BL30].Initialize(Flag_BL30, ( -30.0, pitch_width/2.0+pitch_margin ), rotation)  # Flag_BL30 
        self.mMarkerObservers[Flag_BL20].Initialize(Flag_BL20, ( -20.0, pitch_width/2.0+pitch_margin ), rotation)  # Flag_BL20 
        self.mMarkerObservers[Flag_BL10].Initialize(Flag_BL10, ( -10.0, pitch_width/2.0+pitch_margin ), rotation)  # Flag_BL10 
        self.mMarkerObservers[Flag_B0  ].Initialize(Flag_B0  , (   0.0, pitch_width/2.0+pitch_margin ), rotation)  # Flag_B0 
        self.mMarkerObservers[Flag_BR10].Initialize(Flag_BR10, (  10.0, pitch_width/2.0+pitch_margin ), rotation)  # Flag_BR10 
        self.mMarkerObservers[Flag_BR20].Initialize(Flag_BR20, (  20.0, pitch_width/2.0+pitch_margin ), rotation)  # Flag_BR20 
        self.mMarkerObservers[Flag_BR30].Initialize(Flag_BR30, (  30.0, pitch_width/2.0+pitch_margin ), rotation)  # Flag_BR30 
        self.mMarkerObservers[Flag_BR40].Initialize(Flag_BR40, (  40.0, pitch_width/2.0+pitch_margin ), rotation)  # Flag_BR40 
        self.mMarkerObservers[Flag_BR50].Initialize(Flag_BR50, (  50.0, pitch_width/2.0+pitch_margin ), rotation)  # Flag_BR50 

        # left field flags
        self.mMarkerObservers[Flag_LT30].Initialize(Flag_LT30, ( -pitch_length/2.0-pitch_margin, -30 ), rotation)  # Flag_LT30 
        self.mMarkerObservers[Flag_LT20].Initialize(Flag_LT20, ( -pitch_length/2.0-pitch_margin, -20 ), rotation)  # Flag_LT20 
        self.mMarkerObservers[Flag_LT10].Initialize(Flag_LT10, ( -pitch_length/2.0-pitch_margin, -10 ), rotation)  # Flag_LT10 
        self.mMarkerObservers[Flag_L0  ].Initialize(Flag_L0  , ( -pitch_length/2.0-pitch_margin,   0 ), rotation)  # Flag_L0 
        self.mMarkerObservers[Flag_LB10].Initialize(Flag_LB10, ( -pitch_length/2.0-pitch_margin,  10 ), rotation)  # Flag_LB10 
        self.mMarkerObservers[Flag_LB20].Initialize(Flag_LB20, ( -pitch_length/2.0-pitch_margin,  20 ), rotation)  # Flag_LB20 
        self.mMarkerObservers[Flag_LB30].Initialize(Flag_LB30, ( -pitch_length/2.0-pitch_margin,  30 ), rotation)  # Flag_LB30 

        # right field flags
        self.mMarkerObservers[Flag_RT30].Initialize(Flag_RT30, ( pitch_length/2.0+pitch_margin, -30 ), rotation)  # Flag_RT30 
        self.mMarkerObservers[Flag_RT20].Initialize(Flag_RT20, ( pitch_length/2.0+pitch_margin, -20 ), rotation)  # Flag_RT20 
        self.mMarkerObservers[Flag_RT10].Initialize(Flag_RT10, ( pitch_length/2.0+pitch_margin, -10 ), rotation)  # Flag_RT10 
        self.mMarkerObservers[Flag_R0  ].Initialize(Flag_R0  , ( pitch_length/2.0+pitch_margin,   0 ), rotation)  # Flag_R0 
        self.mMarkerObservers[Flag_RB10].Initialize(Flag_RB10, ( pitch_length/2.0+pitch_margin,  10 ), rotation)  # Flag_RB10 
        self.mMarkerObservers[Flag_RB20].Initialize(Flag_RB20, ( pitch_length/2.0+pitch_margin,  20 ), rotation)  # Flag_RB20 
        self.mMarkerObservers[Flag_RB30].Initialize(Flag_RB30, ( pitch_length/2.0+pitch_margin,  30 ), rotation) # Flag_RB30 

        self.mLineObservers[SL_Left  ].Initialize(SL_Left  , ( -pitch_length/2.0,  0.0 ), rotation) # SL_Left 
        self.mLineObservers[SL_Right ].Initialize(SL_Right , ( pitch_length/2.0,  0.0 ), rotation) # SL_Right 
        self.mLineObservers[SL_Top   ].Initialize(SL_Top   , ( 0.0, -pitch_width/2.0 ), rotation) # SL_Top 
        self.mLineObservers[SL_Bottom].Initialize(SL_Bottom, ( 0.0,  pitch_width/2.0 ), rotation) # SL_Bottom 


