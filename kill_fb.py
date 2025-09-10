#!/bin/bash

SCRIPT="/home/ubuntu/repos/fernbot/fb.py"
LOGFILE="/home/ubuntu/repos/fernbot/fb_monitor.log"

if pgrep -f "$SCRIPT" > /dev/null; then
    echo "$(date): Stopping fb.py..." >> "$LOGFILE"
    pkill -f "$SCRIPT"
else
    echo "$(date): fb.py not running, nothing to stop." >> "$LOGFILE"
fi

