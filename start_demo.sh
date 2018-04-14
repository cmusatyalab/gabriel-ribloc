#! /bin/bash

set -e

function die { echo $1; exit 42; }
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "working directory $DIR"
# Dependency checks
# source torch if user indicates it's not activated by default
if [ -z ${GABRIELPATH+x} ]
then
   die "Gabriel Not Found. Please specify environment variable GABRIELPATH to be Gabriel's root directory";
else
   echo "User specified Gabriel at ${GABRIELPATH}";
fi

echo "launching Gabriel at ${GABRIELPATH}"
cd $GABRIELPATH/server/bin
./gabriel-control &> /tmp/gabriel-control.log &
sleep 5
# NOTE: if the default interface is not eth0 network/util.py change get_ip default interface
./gabriel-ucomm -s 127.0.0.1:8021 &> /tmp/gabriel-ucomm.log &
sleep 5


if pgrep -f "gabriel-ucomm" > /dev/null
then
    cd $DIR
    ./ribloc -p
fi

wait
