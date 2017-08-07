

from twisted.internet import task
from twisted.internet import reactor

def runEvery100ms():
    # print "runEvery100ms"
    pass

def startTask():
    l = task.LoopingCall( runEvery100ms )
    l.start( 0.1 ) # call every 0.1 sec


if __name__ == '__main__':
    
    from client import udpClient, client , ServerParam 

    # must init before use ServerParam and PlayerParam 
    ServerParam.init( 1 , ["rcss"] )
    
    send2server  = udpClient.startUDP() 

    player = client.Client( send2server  )
    udpClient.setDataReceiveCallback( player.receiveFromServer )
    player.SendInitialLizeMsg()

    startTask() 

    reactor.run()
    print 'done'
