from __future__ import division

import numpy as np
from numpy import linalg as LA
import sys
import sympy

FLOAT_EPS =  0.000006

Rad2Deg = np.degrees
Deg2Rad = np.radians

log = np.log


Atan = lambda x:  Rad2Deg( np.arctan(x) )
Atan2 = lambda y,x:  Rad2Deg( np.arctan2(y,x) )

def Sin( v ):
    if isinstance(v, tuple) :
        return v[0]
    else :
        return np.sin(Deg2Rad(v))

def Cos( v ):
    if isinstance(v, tuple) :
        return v[1]
    else :
        return np.cos(Deg2Rad(v))


def SinCos( angleDeg):
    return ( Sin( angleDeg ) , Cos( angleDeg ) )
    


class _NpVector( np.ndarray ) :
    def __eq__(self, obj):
        # return self[0] == obj[0] and self[1] == obj[1]
        return all( super(_NpVector,self).__eq__(obj))

    def __ne__(self,obj):
        return any( super(_NpVector,self).__ne__(obj) )
        
    # std::ostream& operator<<(std::ostream & os, const Vector & v) { return os << "(" << v.mX << ", " << v.mY << ")"; }
    
    def Mod(self): # sqrt
        return LA.norm( self ) 
    def Mod2(self): # x*x + y*y
        return np.dot( self,self )

    def Dist(self, obj):
        return (self-obj).Mod()
    def Dist2(self, obj):
        return (self-obj).Mod2()

    def Dir(self):  # angle in degree
        return  Atan2( self[1],self[0] )
    
    def SetLength( self , length ):
        magnitude = self.Mod()
        if( magnitude > 0 ) :
            return self.copy() * length / magnitude 
        else:
            return Vector( 0,0 ) 
    def Normalize(self):
        return self.SetLength( 1.0 ) 

    def Rotate( self, v  ):
        if isinstance( v , tuple ) :
            return Vector(self[0]* Cos(v) - self[1]* Sin(v), self[1]* Cos(v) + self[0]* Sin(v))
        else:
            return self.Rotate( SinCos( v ) )        

    def ApproxEqual(self, obj):
        return all(np.abs( (self - obj ) ) < FLOAT_EPS  )

_NpVector.X = lambda self : self[0]
_NpVector.Y = lambda self : self[1]

_NpVector.SetX = lambda self,x: self.__setitem__( 0, x )
_NpVector.SetY = lambda self,y: self.__setitem__( 1, y )

_NpVector.SetValue = lambda self,x,y: [self.__setitem__( 0, x ) , self.__setitem__( 1, y )][-1]



def Vector( x,y) :
    vec = _NpVector( 2 , dtype=float )
    vec[0] = x
    vec[1] = y
    return vec

class Line(object) :
    # ax + by + c = 0
    # def __init__(self ,a,b,c  ) :
    #     self.mA = a 
    #     self.mB = b
    #     self.mC = c

    def __init__(self, point1 , point2 = None):
        if not point2 is None:
            self.line = sympy.Line( point1 , point2  )
            self.mA , self.mB , self.mC =  [ float(i) for i in self.line.coefficients ] 
        else:
            ray = point1
            self.line = sympy.Line( ray.ray )
            self.mA , self.mB , self.mC = [ float(i) for i in self.line.coefficients ]


    def A(self): return self.mA 
    def B(self): return self.mB 
    def C(self): return self.mC 

    def Dir(self):
        return Atan2( -self.mA , self.mB  )
    def GetX(self , y) :
        return 0.0 if self.mA == 0.0 else -( self.mB*y + self.mC  ) / self.mA 
    def GetY(self , x) :
        return 0.0 if self.mB == 0.0 else -( self.mA*x + self.mC  ) / self.mB 
        
    def IsOnline( self, point ,  eps = FLOAT_EPS ) :
        # return self.line.contains( point )
        return abs( self.mA * point.X() + self.mB * point.Y() + self. mC) < eps
    def IsUpLine( self, point ) :
        # < 0 means upper , > 0 means lower
        return   not self.IsOnline( point ) and (self.mA * point.X() + self.mB * point.Y() + self.mC < 0)

    def HalfPlaneTest(self, pt) :
        if abs(self.mB) > 0.0 :
            print "1:",  pt.Y() , self.GetY(pt.X())
            return pt.Y() > self.GetY(pt.X())
        else:
            # vertical line
            print "2" , pt.X() , -self.mC / self.mA
            return pt.X() < -self.mC / self.mA;
    def IsSameSlope(self,l):
        return self.is_parallel(l)

    def GetProjectPoint(self, point ) :
        pt = self.line.projection( sympy.Point(point) )
        return Vector( float(pt.x) , float(pt.y)  )


import unittest  
class mytest(unittest.TestCase): 
    def setUp(self):  
        pass  
    def tearDown(self):  
        pass  
    def testVector(self):
        for i in xrange( 100 ):
            xy = np.random.randint( -100,100,2 ) 
            xy_float = xy.astype(float)

            vec = Vector( xy[0] , xy[1] )
            vec2 = Vector( xy_float[0] , xy_float[1] )
            
            self.assertEqual( vec.X() , vec2.X()   )
            self.assertEqual( vec2 == vec , True )

            t = -vec 
            t = vec + vec 
            t = vec2 - vec 
            t = vec2 * 3
            t = vec2 / 4
            
            self.assertEqual( vec.Mod() , vec2.Mod()   )
            self.assertEqual( vec.Mod2() , vec2.Mod2()   )

            self.assertEqual( vec.Dist( Vector(-1,-1) ) , vec2.Dist( Vector(-1,-1) )   )
            self.assertEqual( vec.Dist2( Vector(-1,-1) ) , vec2.Dist2( Vector(-1,-1) )   )
              
            self.assertEqual( vec.Dir() , vec2.Dir()   )

            vec.SetLength( 10 ) ; vec2.SetLength( 10 )   
            self.assertEqual( vec2 == vec , True )
            
            vec.Normalize() ; vec2.Normalize();
            self.assertEqual( vec2 == vec , True )
            
            vec.Rotate( 45 ) ; vec2.Rotate( SinCos(45)  )
            self.assertEqual( vec2 == vec , True )
            self.assertEqual( vec2.ApproxEqual( vec ) , True )

            vec.SetY( -101 ) ; vec2.SetY(-101)
            self.assertEqual( vec.Y() , vec2.Y()   )
            vec.SetValue( 101,-101 ) ; vec2.SetValue( 101,-101 )

            vec += vec2 
            vec += 2
            vec /= vec2 
            vec /= 3

            vec2 != vec 
            vec2 != 2

    def testLine(self):
        from sympy import solve
        x,y = sympy.symbols("x , y"  )
        for i in xrange( 100 ):
            xy = np.random.randint( -10,10,2 ).astype(float)
            xy2 = np.random.randint( -10,10,2 ).astype(float)
            if all(xy == xy2 ):
                xy2[0] -=1
            l = Line( Vector( xy[0] , xy[1]) , Vector( xy2[0] , xy2[1])  ) 
            # TODO , ray constructor
            self.assertEqual( l.B() , l.line.coefficients[1] )

            self.assertEqual( l.Dir() , Atan2(-float(l.line.coefficients[0]) , float(l.line.coefficients[1]) )  )
            self.assertEqual( type(l.GetX( 2.5 ) ) , float   )
            
            # print l.line.coefficients
            expr = float( l.line.coefficients[0] ) * x + float(l.line.coefficients[1])*y + float(l.line.coefficients[2])
            sols =  solve(expr.subs( x, 2.5 ))
            sol = sols[0] if len(sols) > 0 else 0.0
            self.assertEqual( (l.GetY( 2.5 ) ) , sol   )

            # print l.line
            self.assertEqual( l.IsOnline( Vector( xy[0]+0.1 , xy[1]+0.00001)) , False )
            self.assertEqual( l.IsOnline( Vector( xy[0] , xy[1])) , True )
            self.assertEqual(  Vector( xy[0] , xy[1]) ,  l.GetProjectPoint( Vector( xy[0] , xy[1])  )  )
            # print l.line , l.line.coefficients ,  l.GetProjectPoint( Vector(1,2) ) 
            self.assertEqual( l.IsOnline( l.GetProjectPoint( Vector(-21,2) ) )  , True )
            l.IsUpLine( Vector(-21,2) )
            print l.line , l.line.coefficients
            self.assertEqual( l.IsUpLine( Vector(-21,2) )   , l.HalfPlaneTest(  Vector(-21,2) )  )
             


if __name__ == '__main__' :
    import time
    np.random.seed(seed=int( time.time() ) ) 
    unittest.main()
