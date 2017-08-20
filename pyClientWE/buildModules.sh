
SRC_PATH="../src"
PYTHON_HEAD="/usr/include/python2.7"

DEFS=-DHAVE_CONFIG_H 
CXX=c++ 
AM_CXXFLAGS="-W -Wall"
CXXFLAGS="-g -O2"

BOOST_FILESYSTEM_LIB="-lboost_filesystem"
BOOST_LDFLAGS="-L/usr/local/lib"
BOOST_SYSTEM_LIB="-lboost_system"
BOOST_LIB="${BOOST_FILESYSTEM_LIB} ${BOOST_LDFLAGS} ${BOOST_SYSTEM_LIB}"

#---------------------------------------------------------------

# module
moduleName="serverparam"
swig -Wall -python -c++  -I${SRC_PATH} -I${PYTHON_HEAD} ${moduleName}.i


# prepare source files
SRC_FILES="${moduleName}_wrap.cxx \
            ${SRC_PATH}/ServerParam.cpp \
            ${SRC_PATH}/ParamEngine.cpp "

# compile
${CXX} -c -fPIC  ${DEFS} ${CXXFLAGS}  ${AM_CXXFLAGS}  -I${PYTHON_HEAD}  -I${SRC_PATH} -I${SRC_PATH}"/.." ${SRC_FILES}

# linking
${CXX}  -dynamiclib -lpython -lz ${BOOST_LIB}  *.o  -o _${moduleName}.so
#---------------------------------------------------------------

# module
moduleName="playerparam"
swig -Wall -python -c++  -I${SRC_PATH} -I${PYTHON_HEAD} ${moduleName}.i


# prepare source files
SRC_FILES="${moduleName}_wrap.cxx \
            ${SRC_PATH}/PlayerParam.cpp "

# compile
${CXX} -c -fPIC  ${DEFS} ${CXXFLAGS}  ${AM_CXXFLAGS}  -I${PYTHON_HEAD}  -I${SRC_PATH} -I${SRC_PATH}"/.." ${SRC_FILES}

# linking
${CXX}  -dynamiclib -lpython -lz ${BOOST_LIB}  *.o  -o _${moduleName}.so



 



