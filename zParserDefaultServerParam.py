import re

RE_PATTERN_DEFAULT_PARAM = re.compile(  r"(\w+)\s+ServerParam\s*::\s*(\w+)\s*=\s*(.*?);"  )



if __name__ == '__main__':
    f_input = "zServer/rcssserver-15.3.0/src/serverparam.cpp"

    dict_keys = {}
    with open(f_input) as fp:
        lines = fp.readlines()
        for line in lines:
            result = RE_PATTERN_DEFAULT_PARAM.search( line )
            if result:
                print result.groups()
            
