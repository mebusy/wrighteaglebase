
from player import Player as cPlayer
from utilities import Time 

class Player( cPlayer ) :
    def __init__(self):
        super(Player, self).__init__()

        self.last_time = Time( -100, 0 )

    def Run(self):
        self.mpObserver.Lock()
        self.mpObserver.UnLock()
        pass
