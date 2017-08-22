
SRC_PATH="../src"
PYTHON_HEAD="/usr/include/python2.7"

DEFS=-DHAVE_CONFIG_H 
CXX=g++ 
# AM_CXXFLAGS="-W -Wall"
CXXFLAGS="-O3 -Wall -c -fmessage-length=0 -MMD -MP"

BOOST_FILESYSTEM_LIB="-lboost_filesystem"
BOOST_LDFLAGS="-L/usr/local/lib"
BOOST_SYSTEM_LIB="-lboost_system"
BOOST_LIB="${BOOST_FILESYSTEM_LIB} ${BOOST_LDFLAGS} ${BOOST_SYSTEM_LIB}"

PRE_BUILT_SO=""

function necessaryObjFiles( )
{
    objfiles=""
    for i in $@ ; do
        # echo $i
        bn=$(basename $i)
        name="${bn%.*}"
        # echo ${name}
        objfiles="${objfiles} ${name}.o"
    done;
    echo ${objfiles}
}

function necessarySrcFiles( )
{
    srcFiles=""
    for i in $@ ; do
        # echo $i
        bn=$(basename $i)
        name="${bn%.*}".o
        
        if [ ! -f "${name}" -o  "$i" -nt "${name}" ]; then
            srcFiles="${srcFiles} $i"
        fi
    done;
    echo ${srcFiles}
}


#---------------------------------------------------------------

function buildModule() 
{
    # module
    moduleName=$1
    echo building ${moduleName} 
    swig -Wall -python -c++ -I${SRC_PATH} -I${PYTHON_HEAD} ${moduleName}.i
    
    shift

    objfiles=$(necessaryObjFiles "$@")
    srcFiles=$(necessarySrcFiles "$@")

    # compile
    ${CXX} -c -fPIC  ${DEFS} ${CXXFLAGS}  -I${PYTHON_HEAD}  -I${SRC_PATH} ${srcFiles}

    # linking
    ${CXX}  -dynamiclib -lpython -lz ${BOOST_LIB}  ${objfiles} ${PRE_BUILT_SO}  -o _${moduleName}.so  

    # for OSX rpath issue
    install_name_tool -id ${PWD}/_${moduleName}.so _${moduleName}.so

    eval so_${moduleName}=_${moduleName}.so
    # PRE_BUILT_SO="${PRE_BUILT_SO} _${moduleName}.so"
}


# if fales; then
#---------------------------------------------------------------
moduleName="paramengine"
SRC_FILES="${moduleName}_wrap.cxx \
            ${SRC_PATH}/ParamEngine.cpp "
buildModule ${moduleName} ${SRC_FILES}

#---------------------------------------------------------------
moduleName="serverparam"
SRC_FILES="${moduleName}_wrap.cxx \
            ${SRC_PATH}/ServerParam.cpp "
PRE_BUILT_SO="${so_paramengine}"
buildModule ${moduleName} ${SRC_FILES}

#---------------------------------------------------------------
moduleName="playerparam"
SRC_FILES="${moduleName}_wrap.cxx \
            ${SRC_PATH}/PlayerParam.cpp "
PRE_BUILT_SO="${so_paramengine} ${so_serverparam}"
buildModule ${moduleName} ${SRC_FILES}

#---------------------------------------------------------------
moduleName="plotter"
SRC_FILES="${moduleName}_wrap.cxx \
            ${SRC_PATH}/Plotter.cpp "
PRE_BUILT_SO="${so_playerparam}"
buildModule ${moduleName} ${SRC_FILES}

#---------------------------------------------------------------
moduleName="geometry"
SRC_FILES="${moduleName}_wrap.cxx \
            ${SRC_PATH}/Geometry.cpp "
PRE_BUILT_SO="${so_plotter}"
buildModule ${moduleName} ${SRC_FILES}

#---------------------------------------------------------------
moduleName="rcsstypes"
SRC_FILES="${moduleName}_wrap.cxx \
            ${SRC_PATH}/Types.cpp "
buildModule ${moduleName} ${SRC_FILES}

#---------------------------------------------------------------
moduleName="udpsocket"
SRC_FILES="${moduleName}_wrap.cxx \
            ${SRC_PATH}/UDPSocket.cpp "
buildModule ${moduleName} ${SRC_FILES}

#---------------------------------------------------------------
moduleName="utilities"
SRC_FILES="${moduleName}_wrap.cxx \
            ${SRC_PATH}/Thread.cpp \
            ${SRC_PATH}/DynamicDebug.cpp \
            ${SRC_PATH}/Utilities.cpp "
PRE_BUILT_SO="${so_playerparam}"
buildModule ${moduleName} ${SRC_FILES}

#---------------------------------------------------------------
moduleName="timetest"
SRC_FILES="${moduleName}_wrap.cxx \
            ${SRC_PATH}/TimeTest.cpp "
PRE_BUILT_SO="${so_playerparam} ${so_utilities}"
buildModule ${moduleName} ${SRC_FILES}

#---------------------------------------------------------------
moduleName="net"
SRC_FILES="${moduleName}_wrap.cxx \
            ${SRC_PATH}/Net.cpp "
buildModule ${moduleName} ${SRC_FILES}

#---------------------------------------------------------------
moduleName="networktest"
SRC_FILES="${moduleName}_wrap.cxx \
            ${SRC_PATH}/NetworkTest.cpp "
buildModule ${moduleName} ${SRC_FILES}

#---------------------------------------------------------------
moduleName="basestate"
SRC_FILES="${moduleName}_wrap.cxx \
            ${SRC_PATH}/BaseState.cpp "
buildModule ${moduleName} ${SRC_FILES}

#---------------------------------------------------------------
# fi

moduleName="observer"
SRC_FILES="${moduleName}_wrap.cxx \
            ${SRC_PATH}/Dasher.cpp \
            ${SRC_PATH}/Tackler.cpp \
            ${SRC_PATH}/BasicCommand.cpp \
            ${SRC_PATH}/Simulator.cpp \
            ${SRC_PATH}/PlayerState.cpp \
            ${SRC_PATH}/DecisionData.cpp \
            ${SRC_PATH}/Logger.cpp \
            ${SRC_PATH}/Strategy.cpp \
            ${SRC_PATH}/PositionInfo.cpp \
            ${SRC_PATH}/Formation.cpp \
            ${SRC_PATH}/FormationTactics.cpp \
            ${SRC_PATH}/InfoState.cpp \
            ${SRC_PATH}/InterceptInfo.cpp \
            ${SRC_PATH}/InterceptModel.cpp \
            ${SRC_PATH}/ActionEffector.cpp \
            ${SRC_PATH}/VisualSystem.cpp \
            ${SRC_PATH}/WorldState.cpp \
            ${SRC_PATH}/Observer.cpp "
PRE_BUILT_SO="${so_serverparam} ${so_utilities} ${so_playerparam} ${so_basestate} ${so_geometry} ${so_udpsocket} ${so_networktest} ${so_plotter} "
buildModule ${moduleName} ${SRC_FILES}

#---------------------------------------------------------------
moduleName="worldmodel"
SRC_FILES="${moduleName}_wrap.cxx \
            ${SRC_PATH}/WorldModel.cpp "
PRE_BUILT_SO="${so_observer} "
buildModule ${moduleName} ${SRC_FILES}


#---------------------------------------------------------------

# module
moduleName="player"
# prepare source files
SRC_FILES="${moduleName}_wrap.cxx \
            ${SRC_PATH}/Analyser.cpp \
            ${SRC_PATH}/Agent.cpp \
            ${SRC_PATH}/BehaviorAttack.cpp \
            ${SRC_PATH}/BehaviorBase.cpp \
            ${SRC_PATH}/BehaviorBlock.cpp \
            ${SRC_PATH}/BehaviorDefense.cpp \
            ${SRC_PATH}/BehaviorDribble.cpp \
            ${SRC_PATH}/BehaviorFormation.cpp \
            ${SRC_PATH}/BehaviorGoalie.cpp \
            ${SRC_PATH}/BehaviorHold.cpp \
            ${SRC_PATH}/BehaviorIntercept.cpp \
            ${SRC_PATH}/BehaviorMark.cpp \
            ${SRC_PATH}/BehaviorPass.cpp \
            ${SRC_PATH}/BehaviorPenalty.cpp \
            ${SRC_PATH}/BehaviorPosition.cpp \
            ${SRC_PATH}/BehaviorSetplay.cpp \
            ${SRC_PATH}/BehaviorShoot.cpp \
            ${SRC_PATH}/Client.cpp \
            ${SRC_PATH}/CommandSender.cpp \
            ${SRC_PATH}/CommunicateSystem.cpp \
            ${SRC_PATH}/DecisionTree.cpp \
            ${SRC_PATH}/DynamicDebug.cpp \
            ${SRC_PATH}/Evaluation.cpp \
            ${SRC_PATH}/Kicker.cpp \
            ${SRC_PATH}/Parser.cpp \
            ${SRC_PATH}/Plotter.cpp \
            ${SRC_PATH}/Player.cpp "
PRE_BUILT_SO="${so_playerparam} ${so_serverparam} ${so_utilities} ${so_timetest} ${so_paramengine} ${so_udpsocket} ${so_geometry} ${so_net} \
              ${so_networktest} ${so_basestate} ${so_observer} ${so_playerstate} ${so_worldmodel}"
buildModule ${moduleName} ${SRC_FILES}




 



