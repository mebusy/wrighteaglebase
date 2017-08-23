
from player import Player as cPlayer
from utilities import Time 
from observer import VisualSystem , Logger 
import observer
from commsystem import CommunicateSystem
from serverparam import ServerParam

class Player( cPlayer ) :
    pass
    def __init__(self):
        super(Player, self).__init__()

        self.last_time = Time( -100, 0 )

    def Run(self):
        self.mpObserver.Lock()

        # the order of following statements MUST NOT change
        observer.cvar.Formation_instance.SetTeammateFormations()
        CommunicateSystem.instance().Update() # parser hear info, it shoud be invoked first
        self.mpAgent.CheckCommands( self.mpObserver)
        self.mpWorldModel.Update(self.mpObserver)

        self.mpObserver.UnLock()
        
        time = self.mpAgent.GetWorldState().CurrentTime()

        if self.last_time.T() >= 0 : 
            if time != Time( self.last_time.T()+1 , 0 ) and time != Time(self.last_time.T(), self.last_time.S() + 1) :
                if time == self.last_time :
                    # otherwise the updating of decision date will cause problem
                    self.mpAgent.World().SetCurrentTime(Time(self.last_time.T(), self.last_time.S() + 1))
        self.last_time = time 


        # TODO 
        # calc opponent role by self, before coach gives us that info
        observer.cvar.Formation_instance.UpdateOpponentRole()
        
        VisualSystem.instance().ResetVisualRequest()
        self.mpDecisionTree.Decision(self.mpAgent)

        VisualSystem.instance().Decision()
        CommunicateSystem.instance().Decision()

        if ServerParam.instance().synchMode():
            self.mpAgent.Done()

        self.mpAgent.SetHistoryActiveBehaviors()
        Logger.instance().LogSight()

        time = 2
        print type(time)
        pass
