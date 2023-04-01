#!/usr/bin/python3

# Load Libs
import RPi.GPIO as GPIO
import os
import time as sleep
import json
from datetime import *
import modules.initStart as initStart
import modules.scharfschaltung as scharfschaltung

# Melderabfrage-Modul
import modules.melderabfrage as melderabfrage

# Alarmeingang-Modul ( Dieses Modul definiert, wie auf einen festgestellten Alarm reagiert werden soll )
import modules.alarmeingang as alarmeingang

# Alarmreset-Modul ( Dieses Modul setzt Alarmbenachrichtigungen zurück, wenn Alarme quittiert wurden)
import modules.alarmreset as alarmreset

# configfile einlesen
configfileobj = open('config/config.json')
config = json.load(configfileobj)
configfileobj.close()

# Nummerierung der GPIO-Pins wie auf dem RPi angezeigt verwenden
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

# Start der Alarmzentrale loggen
os.system('./modules/logger_alarmzentrale.py "System" "Alarmzentrale gestartet"')

# init-Script (Dinge die vor Beginn der Schleife getan werden sollen)
initStart.initStart()

# Beginn
try:
  # Dauerschleife der Alarmzentrale
  while True:
    # Liste zum Sammeln von Alarm-Datensätzen, die ggf. in diesem Schleifendurchlauf festgestellt werden
    # Ein Alarm-Datensatz ist wie folgt aufgebaut:
    # {"BereichsID" : "HausExtern", "MelderID": "Tuer1", "Zeit": "T20230101:1200.000"}
    alarme = []

   # Durchlaufe alle in der config definierten Scharfschaltungsbereiche
    for bereich in config['Scharfschaltungsbereiche']:
      print("----------------------------------------------------------")
      # Ist der Bereich scharfgeschaltet?
      if scharfschaltung.isBereichScharf(bereich['ID']):
        print(bereich['ID'] + " ist SCHARFGESCHALTET!")
        # Der Bereich ist scharf. Durchlaufe alle in der config zu diesem Bereich konfigurierten Melder.
        for melder in bereich['Melder']:
          # Frage den aktuellen Zustand des Melders
          if melderabfrage.isMelderstatusAlarm(melder):
            # Melder meldet ALARM!!! Erzeuge einen Alarm-Datensatz
            alarme.append({"BereichsID": bereich['ID'], "MelderID": melder, "Zeit": datetime.now().isoformat()})
            print("ALARM - " + " Bereich: " + bereich['ID'] + " - MelderID: " + melder)
          else:
            print("Sicher - " + " Bereich: " +  bereich['ID'] + " - MelderID: " + melder)
      else:
        print(bereich['ID'] + " ist unscharf.")

      # alarmreset-Modul ausführen, falls bestehende Alarme für den Bereich quittiert wurden
      alarmreset.checkReset(bereich['ID'])

    # Alarme an das Alarmeinang-Modul melden, wenn welche vorhanden
    if alarme:
      alarmeingang.alarmeingang(alarme)


    # Ende der Hauptschleife erreicht. Nächster Durchlauf in 1. Sekunde (kann bei Bedarf beliebig verändert werden)
    sleep.sleep(1000/1000)

except KeyboardInterrupt:
  GPIO.cleanup()
