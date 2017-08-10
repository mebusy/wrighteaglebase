from playerparam import PlayerParam 
from observer import Observer
from rc_types import *
from rcss import *
import re
from readlisp import readlisp  , writelisp
from worldstate import WorldState 

RE_INIT = re.compile( r"\(init\s+(\w+)(?:\s+(\d+))?(?:\s+(\w+))?\)" )

TRAINER_UNUM = 12

class Parser(object) :

    def __init__(self):
        self.observer = Observer() 

    def ParseInitializeMsg(self,msg):

        r = RE_INIT.match( msg ) 
        if r is None:
            return False 

        play_mode = PM_Null
        my_side = '?'
        my_unum = 0

        _side , _unum , _strPM = r.groups()  

        if _side is not None :  my_side = _side 
        if _unum is not None:  my_unum = _unum 
        if _strPM is not None: play_mode = str2PlayMode( _strPM ) 



        if PlayerParam.instance().isCoach() :
            pass
        elif PlayerParam.instance().isTrainer():
            # trainer is global
            my_side = 'l'   # set trainer on self side
            my_unum = TRAINER_UNUM  # set trainer number as 12
            play_mode = PM_BeforeKickOff 
        else:
            pass 

        # print my_side , my_unum , play_mode  , str2PlayMode( "penalty_score_r" ) == PM_PenaltyScore_Right 
        self.observer.init( my_side , my_unum , play_mode )

    def ParseObjType(self, ObjName ) :
        return str2ObjType( ObjName[0].name ) 

    def ParseObjProperty( self, objInfo  ) :
        prop = {} 

        n = len( objInfo )

        if n == 1: # direction only
            prop[ 'direction' ] = objInfo[0]
        else:
            prop[ 'distance' ] = objInfo[0]
            prop[ 'direction' ] = objInfo[1]

        if n > 2 :
            prop[ 'distance_change' ] = objInfo[2]
            prop[ 'direction_change' ] = objInfo[3]
        if n > 4 : 
            prop[ 'body_direction' ] = objInfo[4]
            prop[ 'face_direction' ] = objInfo[5]

        return prop 



    def ParseSight(self, msg) :
        # (see 0 ((f c t) 30.3 6 0 0) ((f r t) 82.3 2) ((f r b) 108.9 41) ((f g r b) 93.7 28) ((g r) 90 24) ((f g r t) 87.4 20) ((f p r b) 87.4 41) ((f p r c) 75.9 29) ((f p r t) 68 14) ((f t 0) 30 -4) ((f t r 10) 40 -3) ((f t r 20) 49.9 -2) ((f t r 30) 59.7 -2) ((f t r 40) 70.1 -2) ((f t r 50) 79.8 -1) ((f t l 10) 20.1 -6 0 0) ((f t l 20) 10.2 -11 0 0) ((F) 2 -90) ((f b r 50) 109.9 44) ((f r 0) 94.6 23) ((f r t 10) 91.8 17) ((f r t 20) 89.1 11) ((f r t 30) 87.4 5) ((f r b 10) 99.5 28) ((f r b 20) 104.6 33) ((f r b 30) 109.9 37) ((p "teamname" 8) 6 0 0 0 0 0))
        sight_data =  readlisp( msg  )

        time  = int( sight_data [1] ) 
        WorldState.instance().updateServerWorldStateTime( time ) 
        
        # record latest sight time 
        self.observer.lastest_sight_time = max( self.observer.lastest_sight_time, time) 

         
        # sight info will update anyways 
        # value will decide whether to update according to update time
        line_locate = None 
        marker_locate = None

        if self.observer.lastest_sight_time == time :
            self.observer.locateMarker[0] = line_locate 
            self.observer.locateMarker[1] = marker_locate

        for ObjInfo in sight_data[2:]:
            ObjName = ObjInfo[0]

            objType = self.ParseObjType( ObjName )
            # print objType

            if objType == OBJ_Marker:
                s = writelisp( ObjName )
                markerType = str2MarkerType(s)
                # print '\t' , markerType 
            elif objType == OBJ_Line :
                s = writelisp( ObjName ) 
                lineType = str2LineType(s)
                # print '\t' , lineType 
            elif objType == OBJ_Player:
                n = len( ObjName ) 
                teamname = unum = goalie = None
                if n > 1 :
                    teamname = ObjName[1]
                if n > 2 :
                    unum = ObjName[2] 
                if n > 3 :
                    goalie = ObjName[3]  # TODO 

                # print "see a player: " ,  teamname , unum , goalie

            prop = self.ParseObjProperty( ObjInfo[1:] )
            # print prop

            if objType == OBJ_Ball:
                self.observer.ballObserver.update( time  , prop  )
            elif objType == OBJ_Line:
                self.observer.mLineObservers[ lineType ].update( time  , prop  )
                if len( prop ) >= 2:
                    if line_locate is None \
                            or self.observer.mLineObservers[ lineType ].distance.value < self.observer.mLineObservers[ line_locate ].distance.value :
                        line_locate = lineType 
            elif objType == OBJ_Marker:
                self.observer.mMarkerObservers[ markerType ].update( time  , prop  )
                if len( prop ) >= 2:
                    if marker_locate is None \
                            or self.observer.mMarkerObservers[ markerType ].distance.value < self.observer.mMarkerObservers[ marker_locate ].distance.value :
                        marker_locate = markerType 
                    
        if self.observer.lastest_sight_time == time : 
            self.observer.locateMarker[0] = line_locate 
            self.observer.locateMarker[1] = marker_locate
        
            # debug
            # if all( self.observer.locateMarker ):
            #     print "get location marker at " , time 


    def ParseSense( self, msg ) :
        # sense_body 0 (view_mode high normal) (stamina 8000 1 130600) (speed 0 0) (head_angle 0) (kick 0) (dash 0) (turn 0) (say 0) (turn_neck 0) (catch 0) (move 0) (change_view 0) (arm (movable 0) (expires 0) (target 0 0) (count 0)) (focus (target none) (count 0)) (tackle (expires 0) (count 0)) (collision none) (foul  (charged 0) (card none)))
        sense_data =  readlisp( msg  )
        time  = int( sense_data [1] )
        WorldState.instance().updateServerWorldStateTime( time ) 

        # for body data , only un-updated data will be handled
        if time < WorldState.instance().timeUpdated :
            return 
         
        d = {}
        d["time"] = time 


        for item in sense_data[2:]:
            key = item[0]
            if key.name == "collision" :
                # print 'collison  with ' , item[1]
                # d[ key.name ] = item[1].name  # (collision {none|[(ball)][(player)][(post)]})
                pass
            elif len(item) == 2:
                d[ key.name ] = float( item[1]  ) 
            elif key.name == "view_mode":
                d[ key.name ] = eval( item[2].name.upper()  )  # VIEW_QUALITY does not care
            elif key.name == "stamina" :
                d[key.name],d["effort"],d["capacity"] = [ float(i) for i in item[1:] ] 
            elif key.name == "speed" :
                d[key.name],d["speed_dir"] =  [ float(i) for i in item[1:] ] 
            elif key.name == "arm" :
                d[key.name] = {} 
                # (movable 0)  cycles remaining until next arm moving
                # (expires 0)  cycles remaining before arm action failed
                # (target 0 0)  target dist / target dir
                # (count 0)     point count
                for subitem  in item[1:] :
                    if len(subitem) == 2:
                        d[key.name][ subitem[0].name ] = int( subitem[1]  ) 
                    else:
                        # target
                        d[key.name][ subitem[0].name + "dist"] = float( subitem[1]  )
                        d[key.name][ subitem[0].name + "dir"] = float( subitem[2]  )
            elif key.name == "focus" :
                d[key.name] = {} 
                # (focus (target none) (count 0)) 
                for subitem  in item[1:] :
                    if subitem[0].name == "target":
                        d[key.name][ subitem[0].name ] =  subitem[1].name  
                    else:
                        d[key.name][ subitem[0].name ] =  int(subitem[1] ) 
            elif key.name == "tackle" :
                d[key.name] = {} 
                # (tackle (expires 0) (count 0)) 
                for subitem  in item[1:] :
                    d[key.name][ subitem[0].name ] =  int(subitem[1] ) 
            elif key.name == "foul" :
                d[key.name] = {} 
                # (foul  (charged 0) (card none))
                for subitem  in item[1:] :
                    if subitem[0].name == "card":
                        d[key.name][ subitem[0].name ] =  subitem[1].name  
                    else:
                        d[key.name][ subitem[0].name ] =  int(subitem[1] ) 
            else:
                raise Exception( "unknow sense msg:" + key.name  )

        self.observer.recordBodyInfo(d) 

    def ParseSound(self ,msg) :
        # (hear 3000 referee kick_off_r)
        data =  readlisp( msg  )
        
        sender = data[2].name
        message = data[3].name

        if sender == 'referee' :
            self.observer.serverPlayMode = str2PlayMode( message )
            print "from ", sender , message , self.observer.serverPlayMode 



