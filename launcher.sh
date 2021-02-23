#!/bin/sh
#launcher.sh
#navigate to home directory, then to this directory, then execute python script, then back home
log="/home/pi/AutoPark2020_optimization_epidavros/logs/$(date +%Y-%m-%d)_launch.log"
echo $(date): Starting launcher.sh | tee -a "$log"

cd /
cd home/pi/AutoPark2020_optimization_epidavros
sudo python3 EntranceTerminal.py
cd /

echo $(date): Ending launcher.sh | tee -a "$log"
