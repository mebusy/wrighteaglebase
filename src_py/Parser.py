import time,re,sys
import threading
from UDPSocket import UDPSocket
from ServerParam import ServerParam 
from PlayerParam import PlayerParam
from Types import *


class Parser(threading.Thread):

    def __init__(self, observer):
        threading.Thread.__init__(self)
    
        self.mpObserver  = observer 
        self.mHalfTime = 0

        # final code
        UDPSocket.instance().Initial( ServerParam.instance().serverHost() , ServerParam.instance().playerPort()   )        

        self.mBuf = None

        self.mConnectServerOk = False 
        self.mOkMutex = threading.Lock()


        import signal 
        def signal_handler(signal, frame):
            print 'You pressed Ctrl+C!' 
            self.quitApp()
        signal.signal(signal.SIGINT, signal_handler)

        pass

    def quitApp(self):
        from __main__ import callback_queue 
        callback_queue.put(lambda: sys.exit(1) )  
        import sys
        sys.exit(1)  # same as thread.exit() in thread

    def run(self):
        self.mainLoop()

    def mainLoop(self):
        self.ConnectToServer()
        while True:
            print self
            time.sleep(1)

    def ConnectToServer(self):
        self.mOkMutex.acquire()
        self.mConnectServerOk = False
        self.mOkMutex.release()

        self.SendInitialLizeMsg()

        while True:
            print 'connect server, wait 2 receive'
            self.mBuf= UDPSocket.instance().Receive( ) ;
            if self.ParseInitializeMsg( self.mBuf ):
                break


        self.mOkMutex.acquire()
        self.mConnectServerOk = True
        self.mOkMutex.release()

    def SendInitialLizeMsg(self):
        init_string =  "(init {0} (version {1}))" .format( PlayerParam.instance().teamName() ,
            PlayerParam.instance().playerVersion() )
        if UDPSocket.instance().Send( init_string) < 0 :
            print( "send_initialize_message failed"  )
        print init_string

    def ParseInitializeMsg(self, msg) :
        if msg.startswith( "(error" ):
            print msg
            self.quitApp()
        # if isCoach
        # if isTrainer
        my_side, my_unum, play_mode = [ t(s) for t,s in zip((str,int,str),re.search('\(init\s+(\w)\s+(\d+)\s+(\w+)\)',msg).groups()) ] 
        # print my_side, my_unum, play_mode 

        self.mpObserver.SetOurInitSide(my_side) 
        self.mpObserver.SetOurSide(my_side)
        self.mpObserver.SetSelfUnum(my_unum)

        self.mHalfTime += 1 
        
        # if ( play_mode[0] == 'b' || PlayerParam::instance().isCoach()){ /* Before_kick_off */}
        # else:
        self.mpObserver.SetPlayMode(PM_Play_On)
        self.mpObserver.SetServerPlayMode(SPM_PlayOn) 

        return True
