from playerparam import PlayerParam 
class Parser(object) :

    def ParseInitializeMsg(self,msg):
        print "~~~" , msg 
        if PlayerParam.instance().isCoach() :
            pass
        elif PlayerParam.instance().isTrainer():
            pass
        else:
            pass 

        print PlayerParam.instance().playerSpeedMaxDeltaMin()
