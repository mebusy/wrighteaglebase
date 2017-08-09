


SRC_PATH="../zServer/rcssserver-15.3.0/src"
PYTHON_HEAD="/usr/include/python2.7"

swig -Wall -python -c++  -I${SRC_PATH} -I${PYTHON_HEAD}  rcss.i

DEFS=-DHAVE_CONFIG_H 
CXX=c++ 
AM_CXXFLAGS="-W -Wall"
CXXFLAGS="-g -O2"

SRC_FILES="rcss_wrap.cxx ${SRC_PATH}/*.cpp ${SRC_PATH}/clang*.cpp  ${SRC_PATH}/../rcssbase/conf/*.cpp ${SRC_PATH}/../rcssbase/gzip/*.cpp ${SRC_PATH}/../rcssbase/net/*.cpp "   # ${SRC_PATH}/serverparam.cpp  ${SRC_PATH}/playerparam.cpp ${SRC_PATH}/utility.cpp ${SRC_PATH}/csvsaver.cpp"

${CXX} -c -fPIC  ${DEFS} ${CXXFLAGS}  ${AM_CXXFLAGS}  -I${PYTHON_HEAD}  -I${SRC_PATH} -I${SRC_PATH}"/.." ${SRC_FILES}

#link

BOOST_FILESYSTEM_LIB="-lboost_filesystem"
BOOST_LDFLAGS="-L/usr/local/lib"
BOOST_SYSTEM_LIB="-lboost_system"
BOOST_LIB="${BOOST_FILESYSTEM_LIB} ${BOOST_LDFLAGS} ${BOOST_SYSTEM_LIB}"

rm -f main.o
rm -f client.o

${CXX}  -dynamiclib -lpython -lz ${BOOST_LIB}  *.o  -o _rcss.so



rm -f *.o


