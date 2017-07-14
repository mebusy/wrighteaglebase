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
    
def Polar2Vector( mod , ang ) :
    value = SinCos(ang)
    return Vector(mod * Cos(value), mod * Sin(value))

# return : AngleDeg
def GetNormalizeAngleDeg( ang, min_ang=-180.0 ):
    if ang < min_ang:
        while True:
            ang += 360.0
            if ang >= min_ang: break
    else :
        max_ang = 360.0 + min_ang
        while ang >= max_ang:
            ang -= 360.0;
    return ang;    


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

    def __init__(self, point1 , point2 = None , c = None):
        if point2 is not None and c is not None:
            self.mA = point1
            self.mB = point2
            self.mC = c
            
            if self.mB != 0:
                pt1 =  ( 0, -self.mC/self.mB  )
                pt2 =  ( -self.mC/self.mA , 0  ) if self.mA !=0 else ( pt1[0]+1, pt1[1] )
            elif self.mA !=0 :
                pt1 = ( -self.mC/self.mA , 0  )
                pt2 = ( -self.mC/self.mA , 1  )
            else:
                raise Exception( "wrong line formular" )
                
            self.line = sympy.Line( pt1 , pt2   )
            self.mA , self.mB , self.mC = np.asarray( self.line.coefficients , dtype=float )

        elif point2 is not  None: 
            self.line = sympy.Line( point1 , point2  )
            self.mA , self.mB , self.mC =  np.asarray( self.line.coefficients , dtype=float )
        else:
            ray = point1
            self.line = sympy.Line( ray.ray )
            self.mA , self.mB , self.mC = np.asarray( self.line.coefficients , dtype=float )


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
    def HalfPlaneTest ( self, point ) :
        return (self.mA * point.X() + self.mB * point.Y() + self.mC > 0)

    def IsUpLine(self, pt) :
        if self.IsOnline(pt): 
            return False 

        if abs(self.mB) > 0.0 :
            return pt.Y() > self.GetY(pt.X())
        else:
            # vertical line
            return pt.X() < -self.mC / self.mA;
    def IsSameSlope(self,l):
        return self.line.is_parallel(l.line )

    def GetProjectPoint(self, point ) :
        pt = self.line.projection( sympy.Point(point) )
        return Vector( float(pt.x) , float(pt.y)  )

    # end1 , end2 is 2 points on the line
    # check whether  the projection point of pt , is between end1 and end2
    def IsInBetween( self, pt , end1, end2 ):
        assert self.IsOnline( end1 ) and self.IsOnline(end2) 

        project_pt = self.GetProjectPoint(pt) 
        # print np.dot( (project_pt - end1).Normalize(), (project_pt - end2).Normalize()  )
        dist2 = end1.Dist2(end2);
        return (project_pt.Dist2(end1) < dist2+FLOAT_EPS and  project_pt.Dist2(end2) < dist2+FLOAT_EPS)


    def Intersection( self , l_or_ray , pt=None  ) :
        if pt is None:
            _pt = Vector(0,0)
            if self.Intersection( l_or_ray, _pt ) :
                return _pt 
            return Vector( 0,0  )

        if isinstance( l_or_ray , Line ) :
            if self.IsSameSlope( l_or_ray ):
                return False
            
            points = self.line.intersection( l_or_ray.line  )
            if len(points)==0:
                return False 
            pt.SetValue( float( points[0].x) , float( points[0].y)  )

            return True 
            
        else:
            # TODO intersection with ray
            pass

            return True

    def GetClosestPointInBetween(self, pt , end1 , end2) :
        assert self.IsOnline( end1 ) and self.IsOnline(end2) 

        if self.IsInBetween( pt, end1, end2 ) :
            return self.GetProjectPoint(pt)
        elif end1.Dist2(pt) < end2.Dist2(pt) :
            return end1 
        else:
            return end2 
        
    def Dist_old(self, pt ) :
        return abs(self.mA * pt.X() + self.mB * pt.Y() + self.mC) / np.sqrt(self.mA * self.mA + self.mB * self.mB);

    def Dist( self, pt ) :
        return float(self.line.distance( pt ) )

    def IsPointInSameSide_old( self, pt1,  pt2):
        tl = Line (pt1, pt2)
        if self.IsSameSlope(tl): 
            return True
        inter_point = Vector(0,0)
        self.Intersection(tl, inter_point)
        return (inter_point.X() - pt1.X()) * (pt2.X() - inter_point.X()) <= 0

    def IsPointInSameSide( self, pt1,  pt2): 
        if self.IsOnline(pt1) or  self.IsOnline(pt2) :
            return True
        return self.IsUpLine(pt1) == self.IsUpLine( pt2 ) 
        
    def GetPerpendicular( self,  pt):
        return Line(self.mB, -self.mA, self.mA * pt.Y() - self.mB * pt.X());

    def GetPerpendicular_sym(self, pt):
        l = self.line.perpendicular_line(  pt  ) 
        a,b,c = np.asarray(l.coefficients, dtype=float )
        return Line( a,b,c   )

    def IsEqual(self, l) :
        return self.line.equals( l.line )  

    def MirrorPoint( self, pt) :
        return self.GetProjectPoint(pt) *2 - pt 

class Ray(object) :
    def __init__(self, origin , direction) :
        self.SetValue(origin, direction)
    def Origin(self): 
        return self.mOrigin
    def Dir(self):
        return self.mDirection
    def SetOrigin(self, origin) :
        self.mOrigin = origin 
    def SetDirection(self, direction):
        self.mDirection = direction 
    def SetValue( self,origin, direction ) :
        self.mOrigin = origin 
        self.mDirection = direction 
    def GetPoint(self,dist) :
        return self.mOrigin + Polar2Vector( dist , self.mDirection )
    def IsInRightDir( self,  point ) :
        return abs(GetNormalizeAngleDeg((point - self.mOrigin).Dir() - self.mDirection)) < 10.0
    def OnRay( self, point , buffer = FLOAT_EPS ) :
        v = point - self.mOrigin 
        return abs(Sin(v.Dir() - self.mDirection) * v.Mod()) < buffer and self.IsInRightDir(point)
        

# =======================================================================================================================================


import unittest  

class mytest(unittest.TestCase): 
    def setUp(self):  
        pass  
    def tearDown(self):  
        pass  
    def _testVector(self):
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

    def _testLine(self):
        from sympy import solve
        x,y = sympy.symbols("x , y"  )
        for i in xrange( 40 ):
            xy = np.random.randint( -10,10,2 ).astype(float)
            xy2 = np.random.randint( -10,10,2 ).astype(float)
            if all(xy == xy2 ):
                xy2[0] -=1
            l = Line( Vector( xy[0] , xy[1]) , Vector( xy2[0] , xy2[1])  ) 
            # TODO , ray constructor
            self.assertEqual( l.B() , l.line.coefficients[1] )

            self.assertEqual( l.Dir() , Atan2(-float(l.line.coefficients[0]) , float(l.line.coefficients[1]) )  )
            # self.assertEqual( type(l.GetX( 2.5 ) ) , float   )
            
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
            # print l.line , l.line.coefficients
            self.assertEqual( ( l.IsUpLine( Vector(-21,2) ) ==  l.HalfPlaneTest(  Vector(-21,2) ) ) ,  l.line.coefficients[1] > 0    )
            l2 = Line( Vector( xy[0] , xy[1]+1) , Vector( xy2[0] , xy2[1]+1)  ) 
            # print l.line.slope , l2.line.slope
            self.assertEqual(  l.IsSameSlope (l2) , True )
            self.assertEqual( l.GetProjectPoint( (xy[0] , xy[1])  ) == Vector( xy[0] , xy[1] ) , True  ) 

            self.assertEqual(l.IsInBetween( Vector( (xy[0]+xy2[0] )/2 ,(xy[1]+xy2[1] )/2   ) ,Vector( xy[0] , xy[1]) , Vector( xy2[0] , xy2[1]) ),True)
            self.assertEqual(l.IsInBetween( Vector( (-xy[0]+2*xy2[0] ) ,(-xy[1]+2*xy2[1])) ,Vector( xy[0] , xy[1]) , Vector( xy2[0] , xy2[1]) ),False)
            self.assertEqual(l.IsInBetween( Vector( (2*xy[0]-xy2[0] ),(2*xy[1]-xy2[1])) ,Vector( xy[0] , xy[1]) , Vector( xy2[0] , xy2[1]) ),False)
            
            l2 = Line( Vector( xy[0] , xy[1]) , Vector( xy2[0] , xy2[1]+20)  ) 
            self.assertEqual( l.Intersection( l2  ) , Vector( xy[0] , xy[1]) if not l.IsSameSlope(l2)  else Vector(0,0)  )

            l.GetClosestPointInBetween( Vector( xy2[0] , xy2[1]-1)  ,  Vector( xy[0] , xy[1]) , Vector( xy2[0] , xy2[1])  )
            self.assertEqual( abs( l.Dist_old( Vector(-21,2)  ) - l.Dist( Vector(-21,2)  )  ) < FLOAT_EPS , True   )
            self.assertEqual( l.IsPointInSameSide( Vector(-21,2) , Vector( -18,6 ) ) , l.IsPointInSameSide_old( Vector(-21,2) , Vector( -18,6 )   )  )

            l.GetPerpendicular_sym(  Vector(-21,2) )
            self.assertEqual(  l.GetPerpendicular( Vector(-21,2) ).IsEqual(  l.GetPerpendicular_sym(  Vector(-21,2) ) ) , True  )

            l.MirrorPoint( Vector(-21,2) ) 
            
    def testRay(self):
        for i in xrange( 40 ):
            r = Ray(Vector (1,2) , 30  ) 
            v0 = Vector( 1 + 100*np.cos(  np.radians(30)  ), 2 + 100*np.sin(  np.radians(30)  )  ) 
            self.assertEqual( r.GetPoint( 100 ) , v0 ) 
            n = np.random.randint( -180,180 ) 
            self.assertEqual( GetNormalizeAngleDeg(n) >= -180 , True  )
            self.assertEqual( GetNormalizeAngleDeg(n) <= 180 , True  )

            v1 = v0 + np.array( [ 1,1 ] )
            # print v1, v0
            self.assertEqual(  r.OnRay(  v0  ) , True )
            self.assertEqual(  r.OnRay(  v1  ) , False )


if __name__ == '__main__' :
    import time
    np.random.seed(seed=int( time.time() ) ) 
    unittest.main()
