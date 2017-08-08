
from rcss import rcssServerParam
from utils import Singleton
import types
import re 

RE_SERVERPARAM = re.compile( r"\((\w+)\s+([^)]+)\)" )

class ServerParam( object ):
    __metaclass__ = Singleton
    
    TEAM_SIZE = 11

    def __init__(self):
        self.playerTypes = {} 

    @classmethod
    def instance(cls):
        return ServerParam() 

    def __getattr__(self, name ):
        item =  rcssServerParam.__dict__.get(name) 
        if item is None:
            raise Exception( "ServerParam has not attr:" + name  )

        if callable(item) :
            return types.MethodType(  item , rcssServerParam.instance()   )
        else:
            return item 

    @classmethod 
    def init( cls,  *arg ) :
        return rcssServerParam.init( *arg ) 
        

    def ParseFromServerMsg(self, msg) :
        result = RE_SERVERPARAM.findall( msg ) 
        args = ["rcss_app" , ] 
        for k, v in result :
            args.append(  "server::{0}={1}".format( k,v ) )
        
        self.paramsFromServer = args 
                
    def ParsePlayerType(self, msg) :
        result = RE_SERVERPARAM.findall( msg ) 

        typeID = None
        dict_type = {}
        for k,v in result:
            if k == 'id':
                typeID = int(v) 
            else:
                dict_type[ k ] = float(v)

        self.playerTypes[ typeID ] = dict_type


