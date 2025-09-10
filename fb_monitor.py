#!/bin/bash

# Path to your Python script
SCRIPT="/home/ubuntu/repos/fernbot/fb.py"
PYTHON="/usr/bin/python3"

# Check if process is running
if ! pgrep -f "$SCRIPT" > /dev/null; then
    echo "$(date): fb.py not running, starting it..." >> /home/ubuntu/repos/fernbot/monitor_log.fern
    cd "/home/ubuntu/repos/fernbot" || exit 1
    nohup "$PYTHON" "$SCRIPT" >> /home/ubuntu/repos/fernbot/monitor_log.fern 2>&1 &
fi

