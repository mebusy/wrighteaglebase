

from twisted.internet import task
from twisted.internet import reactor

def runEvery100ms():
    # print "runEvery100ms"
    pass

def startTask():
    l = task.LoopingCall( runEvery100ms )
    l.start( 0.1 ) # call every 0.1 sec


if __name__ == '__main__':
    

    from client import udpClient, client , serverparam 


    # must init before use ServerParam and PlayerParam 
    serverparam.ServerParam.init( 1 , ["rcss"] )

    # extend PlayerParam
    from rcss import PlayerParam
    inst = PlayerParam.instance() 
    inst.isCoach = lambda o :  False 
    print dir( PlayerParam.instance()  )
    
    # start 
    send2server  = udpClient.startUDP() 

    player = client.Client( send2server  )
    udpClient.setDataReceiveCallback( player.receiveFromServer )
    player.SendInitialLizeMsg()

    startTask() 

    reactor.run()
    print 'done'
