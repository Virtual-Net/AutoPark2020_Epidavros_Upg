import json

with open('/home/pi/AutoPark2020_optimization/TerminalSettings.json') as json_file:
    data = json.load(json_file)
dispensername = data['dispenser-type']
w = exec('workerThreadDispenser' + dispensername)
print(type(w))
