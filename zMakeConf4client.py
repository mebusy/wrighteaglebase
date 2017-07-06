import os 
from os.path import expanduser
import re 


home = expanduser("~")

src_path = os.path.join(  home,   ".rcssserver" )
dest_path = "./conf"

WE_conf = """

trainer_data_file= "./train/train.conf"

#below are parameters just for WrightEagle
our_goalie_unum	        = 1
dynamic_debug_mode      = off
save_server_message     = off
save_sight_log          = off
save_dec_log            = off
save_text_log           = off
save_stat_log           = off
time_test               = off
network_test            = off
use_plotter             = off
use_team_graphic        = off

wait_sight_buffer       = 40
wait_hear_buffer        = 40
wait_time_out           = 10

say_pos_x_eps           = 0.3
say_pos_y_eps           = 0.3
say_ball_speed_eps      = 0.1
say_player_speed_eps    = 0.1
say_dir_eps             = 1.0

player_version          = 15.1
coach_version           = 15.1

kicker_mode             = 0
shoot_max_distance = 32.5

"""


def makeServerConf():
    server_file = "server.conf"
    src = os.path.join( src_path, server_file )
    with open( src ) as fp:
        data = fp.read()
        RE_PATTERN_CONF = re.compile( r"\nserver::(\w+\s*=\s*.+)" )
        results = RE_PATTERN_CONF.findall( data )
        print results , len(results )
        dest = os.path.join( dest_path , server_file ) 

        with open(dest, "w") as fpw :
            for result in results:
                fpw.write( result + "\n" )

         

def makePlayerConf():
    player_file = "player.conf"
    src = os.path.join( src_path, player_file )
    with open( src ) as fp:
        data = fp.read()
        RE_PATTERN_CONF = re.compile( r"\nplayer::(\w+\s*=\s*.+)" )
        results = RE_PATTERN_CONF.findall( data )
        print results , len(results )
        dest = os.path.join( dest_path , player_file ) 

        with open(dest, "w") as fpw :
            for result in results:
                fpw.write( result + "\n" )
            fpw.write( WE_conf ) 


if __name__ == '__main__':
    makeServerConf()
    makePlayerConf()
