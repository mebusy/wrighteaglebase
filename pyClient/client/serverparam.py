
from rcss import rcssServerParam
from utils import Singleton
import types  # used to bind a instance to a classmethod 
import re 

RE_SERVERPARAM = re.compile( r"\((\w+)\s+([^)]+)\)" )

class ServerParam( object ):
    __metaclass__ = Singleton
    
    TEAM_SIZE = 11

    def __init__(self):
        self.playerTypes = {} 
        self.paramsFromServer = None 

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
        
    def initParamFromServer(self ) :
        from playerparam import PlayerParam
        allParams = [ "rcss_app" ]
        allParams.extend( ServerParam.instance().paramsFromServer  )
        allParams.extend( PlayerParam.instance().paramsFromServer ) 
        # print allParams 
        ServerParam.init( len( allParams  ) , allParams    ) 
        # print "init server / player param . from " , self.__class__
          

    def ParseFromServerMsg(self, msg) :
        result = RE_SERVERPARAM.findall( msg ) 
        args = [] 
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


