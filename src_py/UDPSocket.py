from socket import *
from utils import * 

class UDPSocket(object):
    __metaclass__ = Singleton
    
    @classmethod
    def instance(cls):
        return UDPSocket()

    
    def Initial(self , host, port  ):
        self.server_host = host
        self.server_port = port 
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)

    def Send(self,msg):
        return self.clientSocket.sendto( msg , (self.server_host, self.server_port)  )

        
    def Receive(self, bufsize=8192 ):
        dat = self.clientSocket.recv( bufsize )
        print "receive", dat 
        return dat



