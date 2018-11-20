#!/bin/bash

echo "starting Chromium"

while true; do
  # kill previous chromium
  killall -9 chromium-browser 2>/dev/null;

  #launch unclutter
 # unclutter &

  # launch browser
  DISPLAY=:0 chromium-browser --incognito --kiosk --disable-translate --disable-cache --disk-cache-size=1 --start-fullscreen --disable-session-crashed-bubble --disable-infobars http://localhost:8000/index.html

done;
