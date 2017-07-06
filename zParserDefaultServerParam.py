import re

RE_PATTERN_DEFAULT_PARAM = re.compile(  r"(\w+)\s+ServerParam\s*::\s*(\w+)\s*=\s*(.*?);"  )



if __name__ == '__main__':
    f_input = "src/ServerParam.cpp" 
    f_output = "zDefaultParam/DefaultServerParam.txt"

    output = ""
    keys = []
    with open(f_input) as fp:
        lines = fp.readlines()
        for line in lines:
            result = RE_PATTERN_DEFAULT_PARAM.search( line )
            if result:
                c_type, key , v = result.groups()
                py_type = "str"
                if c_type == "int":
                    py_type = "int" 
                elif c_type == 'double' or c_type == 'float':
                    py_type = "float"
                elif c_type == 'bool':
                    py_type = "bool" 
                    v = 'False' if v == 'false' else 'True'
                else:
                    print line
                    raise Exception( "unknonw type " )
                output += "{0} = {1}({2}) \n".format( key,py_type , v )
                keys.append( key )

    with open( f_output , "w" ) as fp:
        fp.write(output) 

    # add default value
    with open( f_output ) as fp:
        lines = fp.readlines()
        for line in lines:
            exec(line) 

    # check missing value in server.conf
    dict_conf_keys = {}
    with open( "conf/server.conf" ) as fp:
        lines = fp.readlines()
        for line in lines:
            key = line.split('=')[0].strip() 
            dict_conf_keys[key ] = 1
    for key in keys:
        if not key.lower() in dict_conf_keys:
            print 'missing: ' ,  key 




