from CommandSender import CommandSender 
from Parser import Parser
from Observer import Observer 

class Client(object):
    def __init__(self ) :
        self.mpObserver = Observer()  
        self.mpCommandSender = CommandSender( self.mpObserver )
        self.mpParser = Parser( self.mpObserver  ) 
        self.mpParser.daemon = True

    def RunNormal(self):
        self.mpParser.start()
        pass
