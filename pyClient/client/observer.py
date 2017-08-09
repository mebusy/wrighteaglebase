from serverparam import ServerParam 
from rcss import PM_BeforeKickOff , PM_PlayOn 
from rc_types import *

class objObserver( object ) :
    def __init__(self) :
        self.time = -1

    def update( self, time, prop  ):
        # if time <= self.time :
        #     return 
        # print 'update obj observer' 
        pass
         

class Observer(object):
    
    def __init__(self) :
        self.initialized = False 
        self.initSide = None 
        self.side = None 
        self.unum = None
        self.serverPlayMode = None 
        self.playMode = None

        self.needRotate = False 

        self.time = -1

        self.ballObserver = objObserver() 
        self.mLineObservers = tuple( [ objObserver() for i in xrange(SL_MAX) ]  )  
        self.mMarkerObservers =  tuple( [ objObserver() for i in xrange(FLAG_MAX ) ]  )  
    pass

    # handel init msg
    def init(self, my_side , my_unum , play_mode ):
        self.initSide = my_side 
        self.side = my_side 
        self.unum = my_unum

        if play_mode == PM_BeforeKickOff :
            self.serverPlayMode = play_mode
            self.playMode = play_mode 

            self.kickoffMode = KO_Ours if self.initSide == 'r' else KO_Opps 
        else:
            self.serverPlayMode = PM_PlayOn 
            self.serverPlayMode = PM_PlayOn 

    def Initialize(self) :
        assert self.side is not None

        # if true, multiply all coords by -1 inside initialize
        self.needRotate  = False if self.side == 'r' else True 
        self.InitializeFlags( self.needRotate  ) 
        self.initialized = True 

    def InitializeFlags(self, rotation ) :
        pass 

