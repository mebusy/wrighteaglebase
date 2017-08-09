

from twisted.internet import task
from twisted.internet import reactor


def startTask( callback ):
    l = task.LoopingCall( callback )
    l.start( 0.1 ) # call every 0.1 sec


if __name__ == '__main__':
    

    from client import udpClient, client , serverparam 


    # must init before use ServerParam and PlayerParam 
    serverparam.ServerParam.init( 1 , ["rcss"] )

    # start 
    send2server  = udpClient.startUDP() 

    player = client.Client( send2server  )
    udpClient.setDataReceiveCallback( player.receiveFromServer )
    player.SendInitialLizeMsg()

    startTask( player.plan ) 

    reactor.run()
    print 'done'
