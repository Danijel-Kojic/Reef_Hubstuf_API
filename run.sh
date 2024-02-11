#!/bin/bash

data_dir=~/reef
if [ ! -d $data_dir ]
then
    mkdir -p $data_dir
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR/
current_date=$(date +'%Y-%m-%d')
python3 main.py > $data_dir/${current_date}.html 2>&1