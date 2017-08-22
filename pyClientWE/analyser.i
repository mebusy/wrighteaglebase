%module analyser
%{
#include "Analyser.h"  
%}

%include "mymap.i"

%ignore Analyser::BroadcastPosition();
%include "Analyser.h"



