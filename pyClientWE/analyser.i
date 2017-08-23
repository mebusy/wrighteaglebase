%module analyser
%{
#include "Analyser.h"  
%}

%include "mymap.i"

%ignore Analyser::BroadcastPosition();
/* ignore this method because it is not implemented */

%import(module="utilities") "Utilities.h"
%import(module="observer") "DecisionData.h"
%include "Analyser.h"



