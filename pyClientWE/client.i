%module client
%{
#include "BehaviorBase.h"  
#include "Agent.h"  
#include "Client.h"  
#include "Kicker.h"  
%}

%include "mymap.i"


%immutable BehaviorAttackData::mAgent;
%immutable BehaviorAttackData::mPositionInfo;
%immutable BehaviorAttackData::mInterceptInfo;
%immutable BehaviorAttackData::mStrategy;
%immutable BehaviorAttackData::mFormation;

%immutable BehaviorDefenseData::mAnalyser;

%include "BehaviorBase.h"  
%include "Agent.h"  
%include "Client.h"
%include "Kicker.h"  



