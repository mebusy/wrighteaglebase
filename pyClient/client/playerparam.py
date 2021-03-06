from rcss import rcssPlayerParam 
from utils import Singleton
import types 
from serverparam import RE_SERVERPARAM , ServerParam 

class PlayerParam( object ):
    __metaclass__ = Singleton

    def __init__(self) :
        self.paramsFromServer = None

    @classmethod
    def instance(cls):
        return PlayerParam() 

    def __getattr__(self, name ):
        item =  rcssPlayerParam.__dict__.get(name) 
        if item is None:
            raise Exception( "PlayerParam has not attr:" + name  )

        if callable(item) :
            return types.MethodType(  item , rcssPlayerParam.instance()   )
        else:
            return item 


    def isCoach(self):
        return False 
    
    def isTrainer(self):
        return False 

    def ParseFromServerMsg(self, msg) :
        result = RE_SERVERPARAM.findall( msg ) 
        args = [] 
        for k, v in result :
            args.append(  "player::{0}={1}".format( k,v ) )

        self.paramsFromServer = args 
        


