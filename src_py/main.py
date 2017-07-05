

from Types import ParseEnumType 
ParseEnumType()

from ServerParam import ServerParam 
from PlayerParam import PlayerParam 
from Client import Client
import os ,sys

from utils import * ; 

import Queue
callback_queue = Queue.Queue()

if __name__ == '__main__':
    argvs = []
    

    ServerParam.instance().init( argvs ) 
    #print ServerParam.instance().offside_active_area_size 
    PlayerParam.instance().init( argvs )
    # print PlayerParam.instance().trainer_data_file

    client = Client()
    client.RunNormal()
    
    while True:
        # while blocking , it may not respond to CTRL-C
        try:
            callback = callback_queue.get(False) #blocks until an item is available
            print 'do callback '
            callback()
        except Queue.Empty:
            pass
        import time
        time.sleep(3)

    print 'done'

