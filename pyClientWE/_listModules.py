import glob
import re
import os

RE_MODULE_DEFINE = re.compile( r'%include\s+"(.*?)\.h"\s*' )

def listAllModules():
    files = glob.glob("*.i")
    files.sort()

    allClass = set({})

    for f in files:
        with open( f ) as fp:
            data = fp.read()
            result = RE_MODULE_DEFINE.findall( data ) 
            result.sort()
        
            name , ext = os.path.splitext(f) 
            print name
            for r in result :
                if r in allClass :
                    print "!!! duplicated: " , r  
                else:
                    allClass.add(r)
                print '\t' , r 

            print ''

    for f in files:    
        name , ext = os.path.splitext(f) 
        print "import {0}".format( name )



if __name__ == '__main__':
    listAllModules()
    print '---'
