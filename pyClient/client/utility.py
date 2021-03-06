import math 
from euclid import Vector2

M_PI = 180.0
TWO_PI = 360.0 

def normalize_angle( ang ):
    if abs( ang ) > TWO_PI:
        ang = math.fmod( ang, TWO_PI )

    if ang < -M_PI:  
        ang += TWO_PI
    if ang > M_PI: 
        ang -= TWO_PI

    return ang

def fromPolar_degree( r, degree ) :
    ang = math.radians( degree )
    return Vector2( r * math.cos( ang ), r * math.sin( ang ) )

