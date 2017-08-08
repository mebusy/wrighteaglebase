
_PLAYMODE_STRINGS = [
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
    return _PLAYMODE_STRINGS.index(s) 


KO_Ours = 0 
KO_Opps = 1




