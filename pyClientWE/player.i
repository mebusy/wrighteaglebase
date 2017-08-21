%module(directors="1") player
%{
#include "Player.h"  
%}

%include "mymap.i"

%feature("director") Player ;

%include "Client.h"
%include "Player.h"



