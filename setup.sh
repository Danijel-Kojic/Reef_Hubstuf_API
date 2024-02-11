#!/bin/bash

# Install python dependency libraries
echo "Installing Python3 dependency libraries"
python3 -m pip install -r requirements.txt

# Add a daily cron job
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

command="$SCRIPT_DIR/run.sh"
schedule="0 0 * * *"
echo "Adding daily cron job"
(crontab -l ; echo "$schedule $command") | crontab -
