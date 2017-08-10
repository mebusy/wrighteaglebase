
from utils import Singleton , cUnDelete

class WorldState( cUnDelete ):
    __metaclass__ = Singleton
    
    def __init__(self):
        super( WorldState , self ).__init__()
        self.serverWorldStateTime = -1  # the latest server time 
        self.timeUpdated = -1  # the time agent last updated

    @classmethod
    def instance(cls):
        return WorldState() 

    def updateServerWorldStateTime( self, time ) :
        self.serverWorldStateTime = max( self.serverWorldStateTime , time  )

    def update(self , observer ):
        
        print "last up t:{0},serv t:{1}, sight t:{2} , body t:{3}".format( self.timeUpdated ,self.serverWorldStateTime, observer.lastest_sight_time , "todo" )
        pass



