
class Observer(object):
    def Initialize(self):
        if self.mOurSide == None:
            print "my side unknown, can not initialize"
            return

        rotate = False if self.mOurSide == 'l' else True

    def SetOurInitSide(self, side  ):
        self.mOurInitSide = side

    def SetOurSide(self, side):
        self.mOurSide = side 
        self.mOppSide = 'r' if self.mOurSide == 'l' else  'l'

    def SetSelfUnum(self, unum):
        self.mSelfUnum = unum

    def SetPlayMode(self, play_mode) :
        self.mPlayMode = play_mode

    def SetServerPlayMode(self, server_play_mode):
        self.mServerPlayMode = server_play_mode
