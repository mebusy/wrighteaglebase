%module(directors="1") player
%{
#include "Player.h"  
#include "DecisionTree.h"
%}

%include "mymap.i"

%feature("director") Player ;

%import(module="client") "Client.h" 
%include "Player.h"

%include "DecisionTree.h"



