#!/bin/bash
python master.py &
main_id=$!

trap '{ echo "Exiting program with code 1"; kill $main_id; exit 1; }' INT

while true; do
    rval=0
    rval=$?
    if test -f "./updateNow";
    then
        echo "Checking for updates:"
        rm ./updateNow
        kill $main_id
        git pull
        python master.py &
        main_id=$!
    fi
sleep 1
done
