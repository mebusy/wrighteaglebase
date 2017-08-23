import glob
import re
import os

RE_MODULE_NAME = re.compile( r"%module(?:\s*\(.*?\)\s*)?\s+(\w+)" )
RE_MODULE_DEFINE = re.compile( r'%include\s+"(.*?)\.h"\s*' )

def listAllModules():
    files = glob.glob("*.i")
    files.sort()

    allClass = set({})

    for f in files:
        name , ext = os.path.splitext(f) 
        if name == "mymap":
            continue 

        if not os.path.exists( name.lower() + ".py" ):
            print "moduel {0} error, check it!".format( name )
        with open( f ) as fp:
            data = fp.read()
            
            result = RE_MODULE_NAME.search( data ) 
            if result is None:
                raise Exception( "{0} has no module name ".format(name ) )
            else:
                module_name =  result.groups()[0] 
                if module_name != name :
                    raise Exception( "{0} has a inconsisitant name".format( module_name ) )

            result = RE_MODULE_DEFINE.findall( data ) 
            result.sort()
        
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
