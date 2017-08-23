%module behavior 
%{
#include "BehaviorAttack.h"  
#include "BehaviorBlock.h"  
#include "BehaviorDefense.h"  
#include "BehaviorDribble.h"  
#include "BehaviorFormation.h"  
#include "BehaviorGoalie.h"  
#include "BehaviorHold.h"  
#include "BehaviorIntercept.h"  
#include "BehaviorMark.h"  
#include "BehaviorPass.h"  
#include "BehaviorPenalty.h"  
#include "BehaviorPosition.h"  
#include "BehaviorSetplay.h"  
#include "BehaviorShoot.h"  
#include "Evaluation.h"  
%}

%include "mymap.i"

%import(module="client") "BehaviorBase.h"

%template(BehaviorPlannerBase_A) BehaviorPlannerBase< BehaviorAttackData >;
%template(BehaviorExecuterBase_D) BehaviorExecuterBase< BehaviorDefenseData >;
%template(BehaviorPlannerBase_D) BehaviorPlannerBase< BehaviorDefenseData >;
%template(BehaviorExecuterBase_A) BehaviorExecuterBase< BehaviorAttackData >;


%include "BehaviorAttack.h"  
%include "BehaviorBlock.h"  
%include "BehaviorDefense.h"  
%include "BehaviorDribble.h"  
%include "BehaviorFormation.h"  
%include "BehaviorGoalie.h"  
%include "BehaviorHold.h"  
%include "BehaviorIntercept.h"  
%include "BehaviorMark.h"  
%include "BehaviorPass.h"  
%include "BehaviorPenalty.h"  
%include "BehaviorPosition.h"  
%include "BehaviorSetplay.h"  
%include "BehaviorShoot.h"  
%include "Evaluation.h"  
