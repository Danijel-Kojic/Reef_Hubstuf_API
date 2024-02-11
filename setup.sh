#!/bin/bash

# Install python dependency libraries
python3 -m pip install -r requirements.txt

# Add a daily cron job
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

command="$SCRIPT_DIR/run.sh"
schedule="0 0 * * *"
(crontab -l ; echo "$schedule $command") | crontab -
