import os
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np 

# add pyClientWE/ as python module search path
src_path = os.path.dirname( os.path.abspath(  __file__ ) )
sys.path.append( src_path )
sys.path.append( os.path.normpath( os.path.join( src_path , ".." )) )

os.chdir( os.path.join( os.path.join( src_path , "../.." )  )  )
print "working dir:", os.getcwd()

from geometry import Vector
from behavior import Evaluation
from serverparam import ServerParam 


if __name__ == '__main__' :
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    plus = 5
    step = 0.1

    hw = ServerParam.instance().PITCH_LENGTH * 0.5 + plus
    hh = ServerParam.instance().PITCH_WIDTH * 0.5 + plus

    X = np.arange( -hw, hw, step ) 
    Y = np.arange( -hh, hh , step )  
    xx , yy  = np.meshgrid(X, Y) 

    Z = np.zeros( xx.shape , dtype = xx.dtype ) 
    
    row, col =  Z.shape 

    vec = Vector(0,0) 
    for i in xrange( row ) :
        for j in xrange( col ) :
            x = xx[i,j] 
            y = yy[i,j] 
            vec.SetX(x)
            vec.SetY(y)
            Z[i,j] = v =  Evaluation.instance().EvaluatePosition( vec, False )
        
    surf = ax.plot_surface(xx, yy, Z , 
              cmap=cm.coolwarm, linewidth=0, antialiased=False ) 
    
    # Customize the z axis.
    from matplotlib.ticker import LinearLocator, FormatStrFormatter
    ax.set_zlim(0 , 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))


    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()
    

    print 'done'
