import re
import os


def ParseEnumType():
    mypath = "enum"
    files = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile( os.path.join(mypath, f))]
    # print files
    for file in files:
        with open(file) as fp:
            lines = fp.readlines()
            cnt = 0
            for line in lines:
                line = line.replace("\t","").strip()
                if line != "" :
                    exec( line + " = " + str(cnt) , globals()  ) 
                    cnt +=1
