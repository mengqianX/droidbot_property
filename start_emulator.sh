#!/bin/bash
for ((PORT=5554; PORT<=5584; PORT+=2)); do
    echo start emulator-$PORT...
    emulator -avd Android8.0 -read-only -port $PORT -no-window &
    sleep 2
done