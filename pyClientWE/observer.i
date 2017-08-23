%module observer
%{
#include "Observer.h"  
#include "PlayerState.h"  
#include "Dasher.h"  
#include "Tackler.h"  
#include "Simulator.h"  
#include "Logger.h"  
#include "Strategy.h"  
#include "PositionInfo.h"  
#include "Formation.h"  
#include "FormationTactics.h"  
#include "InfoState.h"  
#include "BasicCommand.h"  
#include "VisualSystem.h"  
#include "InterceptInfo.h"  
#include "InterceptModel.h"  
#include "WorldState.h"  
#include "ActionEffector.h"  
#include "DecisionData.h"  
%}

%include "mymap.i"

%define TEAMSIZE 11 
%enddef



%ignore PlayerState::UpdateTackling(bool);
%ignore PlayerState::UpdateLying(bool);
/* %ignore InfoStateBase; */

%import(module="observer") "BaseState.h"
%import(module="utilities") "Utilities.h"

%include "DecisionData.h"  
%include "Observer.h"
%include "PlayerState.h"
%include "Dasher.h"
%include "Simulator.h"  
%include "Logger.h"  
%include "Strategy.h"  
%include "InfoState.h"  
%include "PositionInfo.h"  
%include "Formation.h"  
%include "FormationTactics.h"  
%include "BasicCommand.h"  
%include "VisualSystem.h"  
%include "InterceptInfo.h"  
%include "InterceptModel.h"  
%include "WorldState.h"  
%include "Tackler.h"  
%include "ActionEffector.h"  


