import sys
import os
import argparse

# add pyClientWE/ as python module search path
src_path = os.path.dirname( os.path.abspath(  __file__ ) )
sys.path.append( src_path )
sys.path.append( os.path.normpath( os.path.join( src_path , ".." )) )

os.chdir( os.path.join( os.path.join( src_path , "../.." )  )  )
print "working dir:", os.getcwd()
# print "sys path:" , sys.path

from serverparam import ServerParam
from playerparam import PlayerParam 
from Player import Player

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-team_name', help='set teamname')   
    parser.add_argument('-host', help='set host')   
    parser.add_argument('-port', help='set port',type=int)   
    parser.add_argument('-coach_port', help='set coach port',type=int)   
    parser.add_argument('-olcoach_port', help='set online coach port',type=int)   
    parser.add_argument('-log_dir', help='set log dir')   
    args = parser.parse_args()

    # print args, dir(args)
    # print args._get_kwargs()
    cargv = ["-{0}={1}".format(k,v)  for k,v in args._get_kwargs()]
    cargv.insert(0,"main")

    ServerParam.instance().init( len(cargv) , cargv )
    PlayerParam.instance().init( len(cargv) , cargv )

    client = Player()
    client.RunNormal()
    print 'done'
