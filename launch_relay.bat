@echo off
echo Starting Relay automation system...

REM Start the Python watcher
cd /d X:\Dev\Relay\watcher
start "" python relay_watcher.py

REM Launch the Relay Tray executable (you'll need to build it first!)
cd /d X:\Dev\Relay\tray\dist
start "" "Relay Tray.exe"

exit