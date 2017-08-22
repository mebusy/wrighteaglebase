
from player import Player as cPlayer
from utilities import Time 
from observer import Formation
from commsystem import CommunicateSystem

class Player( cPlayer ) :
    pass
    def __init__(self):
        super(Player, self).__init__()

        self.last_time = Time( -100, 0 )

    def Run(self):
        self.mpObserver.Lock()

        Formation.instance.SetTeammateFormations()
        # CommunicateSystem.instance().Update()
        # self.mpAgent.CheckCommands( self.mpObserver)
        # self.mpWorldModel.Update(self.mpObserver)

        self.mpObserver.UnLock()
        pass
