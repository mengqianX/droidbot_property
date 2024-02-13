#!/bin/bash
devices=`adb devices`

for device in $devices; do
    if [[ "$device" =~ "emulator-" ]]; then
      adb -s $device emu kill
      echo $device removed
    fi    
done    
echo "All Done."