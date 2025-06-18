#!/usr/bin/bash

set -e

if [ -z "$1" ]; then
    echo "missing command"
    exit 1
fi

if [ -z "$2" ]; then
    echo "missing binary path"
    exit 1
fi

CMD="$1"
BIN="$PWD/bin/$2"

get_pid_by_full_path() {        
    if [ -z "$1" ]; then
        echo "Error：require binary name" >&2
        exit 1
    fi

    APP=`realpath "$1"`
    ps -ww -e -o pid | awk 'NR>1 {print $0}' | while read -r line; do
        path=$(readlink -f "/proc/${line}/exe" 2>/dev/null | sed 's/ (deleted)$//')
        if [ -z "$path" ]; then
            continue
        fi
        if [ "$APP" != "$path" ]; then
            continue
        fi
        echo "$line"
    done
}


PIDS=$(get_pid_by_full_path "$BIN")
case "$CMD" in 
    start)    
        if [ -z "$3" ]; then
            echo "missing config"
            exit 1
        fi
        CFG="$PWD/config/$3"
        echo starting service: "(pwd=$PWD)" "$BIN" -h "$PWD" -c "$CFG"
        ulimit -n 99999
        nohup "$BIN" -h "$PWD" -c "$CFG" > /dev/null 2>&1 &
        ;;
    stop)
        if [ -z "$PIDS" ]; then 
            echo "no previous service process found"
        else
            echo "$PIDS" | while read -r line; do 
                echo killing process $line ...
                $(kill -9 $line)
            done
        fi
        ;;
    status)
        if [ -z $PIDS ]; then
            echo "no previous service process found"
        else
            echo "$PIDS" | while read -r line; do 
                echo "service status: active, pid: " $line
            done
        fi
        ;;
esac

