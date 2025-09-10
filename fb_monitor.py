#!/bin/bash

# Path to your Python script
SCRIPT="/home/ubuntu/repos/fernbot/fb.py"
PYTHON="/usr/bin/python3"

# Check if process is running
if ! pgrep -f "$SCRIPT" > /dev/null; then
    echo "$(date): fb.py not running, starting it..." >> /var/log/fb_monitor.log
    nohup "$PYTHON" "$SCRIPT" >/dev/null 2>&1 &
fi

