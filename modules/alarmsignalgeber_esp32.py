#!/bin/python3

# Dieses Script dient Ansteuern eines Signalgebers mit Blitz und Sirene an ESP32 GPIOs 
# die über eine Rest-API des ESP32 low oder high geschaltet werden können
# Die IP-Adresse es ESP32 wird in sys.argv[1] definiert, z.b "192.168.0.101".
# Der Blitz wird auf sys.argv[2], die Sirene auf sys.argv[3] definiert.
# Der Blitz bleibt dauerhaft aktiviert, die Sirene auf sys.argv[3] wird nach einer definierten Zeit in Sekunden sys.argv[4] wieder deaktivert
#
# Dieses Script ist nicht zum Einbinden als Modul in andere Scripte vorgesehen! Es sollte aus anderen Scripten wie folgt aufgerufen werden:
# os.system(./modules/alarmsignalgeber_esp32.py 192.168.0.101 20 21 180) --> Bedeutet beispielsweise ESP32 mit der IP 192.168.0.101, Blitz auf GPIO20, 
# Sirene auf GPIO21, Sirene für 180 Sekunden aktivieren

import sys
import requests
import json
import time


# Blitz aktivieren
try:
  response = requests.get('http://' + str(sys.argv[1]) + '/api/g' + str(sys.argv[2]) + '/low', timeout=2)
  zustandblitz = response.json()['zustand']
except:
  # Es kann durchaus mal vorkommen, dass der ESP32 nach 2 Sekunden noch nicht bereit ist zum Antworten, probiere erneut
  try:
    sleep.sleep(1)
    response = requests.get('http://' + str(sys.argv[1]) + '/api/g' + str(sys.argv[2]) + '/low', timeout=2)
    zustandblitz = response.json()['zustand']
  except:
    # Immer noch kein Lebenszeichen. zustand = 1 da auf low schalten nicht geklappt hat
    zustand = 1


# Sirene aktivieren
try:
  response = requests.get('http://' + str(sys.argv[1]) + '/api/g' + str(sys.argv[3]) + '/low', timeout=2)
  zustandsirene = response.json()['zustand']
except:
  # Es kann durchaus mal vorkommen, dass der ESP32 nach 2 Sekunden noch nicht bereit ist zum Antworten, probiere erneut
  try:
    sleep.sleep(1)
    response = requests.get('http://' + str(sys.argv[1]) + '/api/g' + str(sys.argv[4]) + '/low', timeout=2)
    zustandsirene = response.json()['zustand']
  except:
    # Immer noch kein Lebenszeichen. zustand = 1 da auf low schalten nicht geklappt hat
    zustandsirene = 1

# In sys.argv[4] definierte Anzahl an Sekunden abwarten
time.sleep(int(sys.argv[4]))


# Sirene deaktivieren
try:
  response = requests.get('http://' + str(sys.argv[1]) + '/api/g' + str(sys.argv[3]) + '/high', timeout=2)
  zustandsirene = response.json()['zustand']
except:
  # Es kann durchaus mal vorkommen, dass der ESP32 nach 2 Sekunden noch nicht bereit ist zum Antworten, probiere erneut
  try:
    sleep.sleep(1)
    response = requests.get('http://' + str(sys.argv[1]) + '/api/g' + str(sys.argv[4]) + '/high', timeout=2)
    zustandsirene = response.json()['zustand']
  except:
    # Immer noch kein Lebenszeichen. zustand = 1 da auf low schalten nicht geklappt hat
    zustandsirene = 1
