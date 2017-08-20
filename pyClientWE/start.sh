
HOST="localhost"
PORT="6000"
VERSION="Release"
BINARY="WEBase"
TEAM_NAME="WEBase"


LOG_DIR="Logfiles"
mkdir $LOG_DIR 2>/dev/null


COACH_PORT=`expr $PORT + 1`
OLCOACH_PORT=`expr $PORT + 2`
N_PARAM="-team_name $TEAM_NAME -host $HOST -port $PORT -coach_port $COACH_PORT -olcoach_port $OLCOACH_PORT -log_dir $LOG_DIR"
G_PARAM="$N_PARAM -goalie on"
C_PARAM="$N_PARAM -coach on"

python src/main.py $N_PARAM

