
SRC_PATH="../zServer/rcssserver-15.3.0/src"
PYTHON_HEAD="/usr/include/python2.7"

swig -Wall -python -c++  -I${SRC_PATH} -I${PYTHON_HEAD}  rcss.i

DEFS=-DHAVE_CONFIG_H 
CXX=c++ 
AM_CXXFLAGS="-W -Wall"
CXXFLAGS="-g -O2"

SRC_FILES="rcss_wrap.cxx ${SRC_PATH}/serverparam.cpp"

${CXX} -c -fPIC  ${DEFS} ${AM_CXXFLAGS}  -I${PYTHON_HEAD}  -I${SRC_PATH} -I${SRC_PATH}"/.." ${SRC_FILES}





rm -f *.o
rm -f *_wrap.cxx


