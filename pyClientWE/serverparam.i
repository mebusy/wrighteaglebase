%module serverparam
%{
#include "ServerParam.h"  
%}

%include "mymap.i"

%import(module="paramengine") "ParamEngine.h"
%include "ServerParam.h"



