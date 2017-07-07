from __future__ import division

from utils import * ;

class PlayerParam(object):
    __metaclass__ = Singleton
    
    @classmethod
    def instance(cls):
        return PlayerParam()

    def __init__(self):
        print 'PlayerParam construct'
        # private
        self.server_conf = "../conf/player.conf"

        with open( self.server_conf ) as fp:
            lines = fp.readlines()
            for line in lines:
                exec(line.replace( "false","False" ).replace( "true", "True" )
                    .replace( "off","False" ), self.__dict__)  
    
    def init(self , argvs  ):
        # TODO
        self.ParseFromCmdLine(  argvs )
        self.MaintainConsistency() 

    def teamName(self):
        return "faketeamname"

    def playerVersion(self):
        return self.player_version 

    def ParseFromCmdLine( self,  argvs )  :
        pass

    def MaintainConsistency(self):
        pass
    
