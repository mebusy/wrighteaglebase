from __future__ import division

from utils import * 
from Geometry import *
import numpy as np 

class ServerParam(object):
    __metaclass__ = Singleton
    
    @classmethod
    def instance(cls):
        return ServerParam()

    def __init__(self):
        print 'ServerParam construct'
        print 1/5
        
        # load default value
        f_input = "../zDefaultParam/DefaultServerParam.txt" 
        with open( f_input ) as fp:
            lines = fp.readlines()
            for line in lines:
                # print line
                k,v =  line.split('=')
                # store constant in both cls and instance namespace
                exec( line , globals()  )
                exec( line ,  self.__dict__   )
                # lower case instance field
                exec ( "{0} = {1}".format( k.lower() , v ) , self.__dict__   )


        # print STAMINA_MAX
        # print self.stamina_max
         
        # load from config file
        # private
        self.server_conf = "../conf/server.conf"
        self.ball_decay_array = np.zeros( 100 )

        
        with open( self.server_conf ) as fp:
            lines = fp.readlines()
            for line in lines:
                exec(line.replace( "false","False" ).replace( "true", "True" ), self.__dict__)  
    
    def init(self , argvs  ):
        # TODO
        self.ParseFromCmdLine(  argvs )
        self.MaintainConsistency() 

    def serverHost(self):
        return self.host if hasattr( self, "host" ) else "127.0.0.1"
    def playerPort(self):
        return self.port if hasattr( self, "port" ) else 6000

    def ParseFromCmdLine( self,  argvs )  :
        pass

    def MaintainConsistency(self):
        pass
        self.kickable_area = self.player_size + self.kickable_margin + self.ball_size;
        self.control_radius_width = self.control_radius - self.player_size;

        self.max_catchable_area    = Vector(self.catchable_area_l, 0.5 * self.catchable_area_w).Mod();
        self.one_minus_ball_decay  = 1.0 - self.ball_decay;
        self.log_ball_decay        = log(self.ball_decay);

        self.ball_decay_array[0]   = 1.0;

        for i in xrange( 1,100 ) :
            self.ball_decay_array[i] = self.ball_decay_array[i - 1] * self.ball_decay;

        # set the field information
        self.left_line     = Line(Vector(-PITCH_LENGTH / 2.0, 0.0), Vector(-PITCH_LENGTH / 2.0, 1.0));
        self.right_line    = Line(Vector(PITCH_LENGTH / 2.0, 0.0), Vector(PITCH_LENGTH / 2.0, 1.0));
        self.top_line      = Line(Vector(0.0, -PITCH_WIDTH / 2.0), Vector(1.0, -PITCH_WIDTH / 2.0));
        self.bottom_line      = Line(Vector(0.0, PITCH_WIDTH / 2.0), Vector(1.0, PITCH_WIDTH / 2.0));

        self.pitch_rectanglar  = Rectangular(-PITCH_LENGTH / 2.0, PITCH_LENGTH / 2.0,
            -PITCH_WIDTH / 2.0, PITCH_WIDTH / 2.0);
        self.active_rectanglar = Rectangular(-PITCH_LENGTH / 2.0 + 1.0, PITCH_LENGTH / 2.0 - 1.0,
            -PITCH_WIDTH / 2.0 + 1.0, PITCH_WIDTH / 2.0 - 1.0);
        self.our_penalty_area  = Rectangular(-PITCH_LENGTH / 2.0, -PITCH_LENGTH / 2.0 + PENALTY_AREA_LENGTH,
            -PENALTY_AREA_WIDTH / 2.0, PENALTY_AREA_WIDTH / 2.0);
        self.opp_penalty_area  = Rectangular(PITCH_LENGTH / 2.0 - PENALTY_AREA_LENGTH, PITCH_LENGTH / 2.0,
            -PENALTY_AREA_WIDTH / 2.0, PENALTY_AREA_WIDTH / 2.0);
        self.our_goal_area     = Rectangular(-PITCH_LENGTH / 2.0, -PITCH_LENGTH / 2.0 + GOAL_AREA_LENGTH,
            -GOAL_AREA_WIDTH / 2.0, GOAL_AREA_WIDTH / 2.0);
        self.opp_goal_area     = Rectangular(PITCH_LENGTH / 2.0 - GOAL_AREA_LENGTH, PITCH_LENGTH / 2.0,
            -GOAL_AREA_WIDTH / 2.0, GOAL_AREA_WIDTH / 2.0);

        self.our_left_goal_kick_point  = self.our_goal_area.TopRightCorner();
        self.our_right_goal_kick_point = self.our_goal_area.BottomRightCorner();
        self.opp_left_goal_kick_point  = self.opp_goal_area.TopLeftCorner();
        self.opp_right_goal_kick_point = self.opp_goal_area.BottomLeftCorner();

        self.our_left_goal_post.SetValue(- PITCH_LENGTH / 2.0, - self.goal_width / 2.0);
        self.our_right_goal_post.SetValue(- PITCH_LENGTH / 2.0, self.goal_width / 2.0);
        self.opp_left_goal_post.SetValue(PITCH_LENGTH / 2.0, - self.goal_width / 2.0);
        self.opp_right_goal_post.SetValue(PITCH_LENGTH / 2.0, self.goal_width / 2.0);

        self.pitch_top_left_point      = self.pitch_rectanglar.TopLeftCorner();
        self.pitch_bottom_left_point   = self.pitch_rectanglar.BottomLeftCorner();
        self.pitch_top_right_point     = self.pitch_rectanglar.TopRightCorner();
        self.pitch_bottom_right_point  = self.pitch_rectanglar.BottomRightCorner();

        self.our_goal = Vector(-PITCH_LENGTH / 2.0, 0.0);
        self.opp_goal = Vector(PITCH_LENGTH / 2.0, 0.0);

        self.ball_run_dist_with_max_speed = self.ball_speed_max / self.one_minus_ball_decay;
        self.max_tackle_dist = Sqrt(self.tackle_dist * self.tackle_dist + self.tackle_width * self.tackle_width);

        self.effort_dec_stamina = self.effort_dec_thr * self.stamina_max;
        self.effort_inc_stamina = self.effort_inc_thr * self.stamina_max;
        self.recover_dec_stamina = self.recover_dec_thr * self.stamina_max;

        # self.half_time = self.half_time * 1000 / self.simulator_step;
        # self.extra_half_time = self.extra_half_time * 1000 / self.simulator_step;
        #
        # self.max_tackle_area = 0.0;
        # int exponent = Max(self.foul_exponent, self.tackle_exponent);
        #
        # for (double x = 0.0; x <= self.tackle_dist; x += 0.01) {
        #         for (double y = 0.0; y <= self.tackle_width; y += 0.01) {
        #                 double prob = 1.0 -
        #                                 MinMax(
        #                                         0.0,
        #                                         pow(x / self.tackle_dist, exponent) + pow(y / self.tackle_width, exponent),
        #                                         1.0
        #                                 );
        #
        #                 if (prob > FLOAT_EPS) {
        #                         self.max_tackle_area = Max(self.max_tackle_area, Sqrt(Sqr(x) + Sqr(y)));
        #                 }
        #         }
        # }
            #

