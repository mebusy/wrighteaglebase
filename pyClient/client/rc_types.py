from rcss import *

__PLAYMODE_STRINGS = [
    "",                   
    "before_kick_off",                  
    "time_over",                        
    "play_on",                          
    "kick_off_l",                       
    "kick_off_r",                       
    "kick_in_l",                        
    "kick_in_r",                        
    "free_kick_l",                      
    "free_kick_r",                      
    "corner_kick_l",                    
    "corner_kick_r",                    
    "goal_kick_l",                      
    "goal_kick_r",                      
    "goal_l",                           
    "goal_r",                           
    "drop_ball",                        
    "offside_l",                        
    "offside_r",                        
    "penalty_kick_l",                   
    "penalty_kick_r",                   
    "first_half_over",                  
    "pause",                            
    "human_judge",                      
    "foul_charge_l",                    
    "foul_charge_r",                    
    "foul_push_l",                      
    "foul_push_r",                      
    "foul_multiple_attack_l",           
    "foul_multiple_attack_r",           
    "foul_ballout_l",                   
    "foul_ballout_r",                   
    "back_pass_l",                      
    "back_pass_r",                      
    "free_kick_fault_l",                
    "free_kick_fault_r",                
    "catch_fault_l",                    
    "catch_fault_r",                    
    "indirect_free_kick_l",             
    "indirect_free_kick_r",             
    "penalty_setup_l",                  
    "penalty_setup_r",                  
    "penalty_ready_l",                  
    "penalty_ready_r",                  
    "penalty_taken_l",                  
    "penalty_taken_r",                  
    "penalty_miss_l",                   
    "penalty_miss_r",                   
    "penalty_score_l",                  
    "penalty_score_r"                   
]

def str2PlayMode(s) :
    return __PLAYMODE_STRINGS.index(s) 


KO_Ours = 0 
KO_Opps = 1


__LineType = {
    
    "(l l)"  : SL_Left , 
    "(l r)"  : SL_Right , 
    "(l t)"  : SL_Top , 
    "(l b)"  : SL_Bottom  , 
}

__MarkerTypes = {
    "(g l)"  : Goal_L , 
    "(g r)"  : Goal_R , 


    "(f c)"  : Flag_C , 
    "(f c t)"  : Flag_CT , 
    "(f c b)"  : Flag_CB , 
    "(f l t)"  : Flag_LT , 
    "(f l b)"  : Flag_LB , 
    "(f r t)"  : Flag_RT , 
    "(f r b)"  : Flag_RB , 

    "(f p l t)"  : Flag_PLT , 
    "(f p l c)"  : Flag_PLC , 
    "(f p l b)"  : Flag_PLB , 
    "(f p r t)"  : Flag_PRT , 
    "(f p r c)"  : Flag_PRC , 
    "(f p r b)"  : Flag_PRB , 

    "(f g l t)"  : Flag_GLT , 
    "(f g l b)"  : Flag_GLB , 
    "(f g r t)"  : Flag_GRT , 
    "(f g r b)"  : Flag_GRB , 

    "(f t l 50)"  : Flag_TL50 , 
    "(f t l 40)"  : Flag_TL40 , 
    "(f t l 30)"  : Flag_TL30 , 
    "(f t l 20)"  : Flag_TL20 , 
    "(f t l 10)"  : Flag_TL10 , 
    "(f t 0)"  : Flag_T0 , 
    "(f t r 10)"  : Flag_TR10 , 
    "(f t r 20)"  : Flag_TR20 , 
    "(f t r 30)"  : Flag_TR30 , 
    "(f t r 40)"  : Flag_TR40 , 
    "(f t r 50)"  : Flag_TR50 , 

    "(f b l 50)"  : Flag_BL50 , 
    "(f b l 40)"  : Flag_BL40 , 
    "(f b l 30)"  : Flag_BL30 , 
    "(f b l 20)"  : Flag_BL20 , 
    "(f b l 10)"  : Flag_BL10 , 
    "(f b 0)"  : Flag_B0 , 
    "(f b r 10)"  : Flag_BR10 , 
    "(f b r 20)"  : Flag_BR20 , 
    "(f b r 30)"  : Flag_BR30 , 
    "(f b r 40)"  : Flag_BR40 , 
    "(f b r 50)"  : Flag_BR50 , 

    "(f l t 30)"  : Flag_LT30 , 
    "(f l t 20)"  : Flag_LT20 , 
    "(f l t 10)"  : Flag_LT10 , 
    "(f l 0)"  : Flag_L0 , 
    "(f l b 10)"  : Flag_LB10 , 
    "(f l b 20)"  : Flag_LB20 , 
    "(f l b 30)"  : Flag_LB30 , 

    "(f r t 30)"  : Flag_RT30 , 
    "(f r t 20)"  : Flag_RT20 , 
    "(f r t 10)"  : Flag_RT10 , 
    "(f r 0)"  : Flag_R0 , 
    "(f r b 10)"  : Flag_RB10 , 
    "(f r b 20)"  : Flag_RB20 , 
    "(f r b 30)"  : Flag_RB30 ,  


}

__MarkerTypesReverse = {v: k for k, v in __MarkerTypes.iteritems()}   

__ObjTypes = {
    "l" : OBJ_Line ,

    "b" : OBJ_Ball ,
    "B" : OBJ_Ball ,

    "f" : OBJ_Marker ,
    "g" : OBJ_Marker  ,   

    "F" : OBJ_Marker_Behind ,
    "G" : OBJ_Marker_Behind ,
   
    "p" : OBJ_Player ,
    "P"  : OBJ_Player ,
}

def str2ObjType( s ) :
    return __ObjTypes[s] 

def str2LineType(s) :
    return __LineType[s] 

def str2MarkerType(s) :
    return __MarkerTypes[s] 

def markerType2str(t):
    return __MarkerTypesReverse[t]
    

