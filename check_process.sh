#!/bin/bash

process=`/usr/bin/pgrep serial_read.py`

if [ $process ]
then
    echo "process $process exsits"
else
    echo "we're fucked up"
fi

    
