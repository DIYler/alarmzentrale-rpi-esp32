#!/usr/bin/python3

# Dies ist das alarmeingang-Modul. Es definiert, wie auf einen Alarm reagiert werden soll.
# Alarme werden vom Hauptscript alarmzentrale.py festgestellt.
# alarmzentrale.py erstellt pro Schleifendurch eine Liste von Bereichen und Meldern, die während des Durchlaufs einen Alarm gemeldet haben.
# alarmzentrale.py ruft dann die Methode alarmeingang aus diesem Modul auf und übergibt dabei die Liste.
# Die Liste kann aus mehreren Datensätzen bestehen. Jeder Datensatz beinhaltet die folenden Informationen:
# BereichsID, MelderID, Zeit

# alarmeingang.py hat nun die Aufgabe die Datensätze auszuwerten und die in der config.json definierten Maßnahmen,
# wie zum Beispiel die Aktivierung von Signalgebern und Benachrichtigungen auszuführen.
# Desweiteren meldet alarmzentrale.py bei jedem Schleifendurchlauf immer wieder den selben Bereich und Melder, solange der Melder weiterhin die
# Gefahr feststellt. alarmeingang.py sorgt hier an dieser Stelle dafür, dass die Signalisierungs- und Benachrichtigungsmaßnahmen nicht endlos
# erneut ausgeführt werden, wenn ein Bereich und Melder gemeldet wird, der bereits gemeldet wurde.
# Es steuert auch, welche Maßnahmen wie lange erhalten bleiben. Signalgeber wie Sirenen sollen zum Beispiel nicht dauerhauft aktiviert bleiben,
# um die Nachbarschaft nicht unnötigerweise zu belästigen.  

import os
import json
import RPi.GPIO as GPIO
import time as sleep
import modules.alarmpush as alarmpush # Push via Gotify
import modules.alarmpushover as alarmpushover # Push via Pushover


# Nummerierung der GPIO-Pins wie auf dem RPi angezeigt verwenden
GPIO.setmode(GPIO.BCM)

# config.json einlesen
configfileobj = open('config/config.json')
config = json.load(configfileobj)
configfileobj.close()

# alarmeingang
def alarmeingang(alarmliste):
  for alarm in alarmliste:
    # Prüfe, ob überhaupt schon die Melderdatei in dem gemeldeten Bereich existiert, wenn nicht, lege sie an
    if not os.path.exists('alarme/aktiv/' + alarm['BereichsID'] + "/" + alarm['MelderID']):
      # Melder-Alarmdatei existiert in dem gemeldeten Bereich noch nicht. Lege Melderdatei ein und setze Wert auf 0
      f = open("alarme/aktiv/" + alarm['BereichsID'] + "/" + alarm['MelderID'], "w")
      f.write("0")
      f.close()

    # Prüfen, ob der gemeldete Melder in dem jeweiligen Bereich bereits ausgelöst hat und darauf reagiert wurde
    f = open("alarme/aktiv/" + alarm['BereichsID'] + "/" + alarm['MelderID'], "r")
    if int(f.read()) == 0:
      f.close()
      # !!! ALARM !!! Ein neuer bislang ungemeldeter Alarm liegt vor! Ermittle die Alarmbenachrichtigungswege für den Bereich aus der config.json
      # os.system("./modules/logger_alarmzentrale.py \"Alarm\" \"Alarm im Bereich: " + alarm['BereichsID'] + " durch Melder " + alarm['MelderID'] + " ausgelöst\"")
      benachrichtigungen = next(item for item in config['Scharfschaltungsbereiche'] if item["ID"] == alarm['BereichsID'])["Alarmbenachrichtigungen"] 
      for benachrichtigung in benachrichtigungen:
       # Lade Benachrichtigungsobjekt
       benachrichtigungsobj = next(item for item in config['Alarmbenachrichtigung'] if item["ID"] == benachrichtigung)
       # Typ des Benachrichtigungsobjekt ermitteln
       if benachrichtigungsobj['Typ'] == "alarmpush":
         # Sende einen alarmpush über das alarmpush-module via Gotify
         print("Alarm-Push via Gotify wird gesendet")
         alarmpush.alarmPush("!!!ALARM!!! Bereich: " + alarm['BereichsID'], "!!!ALARM!!! Die Alarmzentrale hat Alarm ausgelöst - Bereich: " + alarm['BereichsID'] + " - Melder: " + alarm['MelderID'])
       elif benachrichtigungsobj['Typ'] == "alarmpushover":
         # Sende einen alarmpush über das alarmpushover-module via Pushover
         alarmpushover.alarmPushover(benachrichtigungsobj['userkey'],"!!!ALARM!!! Bereich: " + alarm['BereichsID'], '<font color="red"><b>!!!ALARM!!!</b></font> Die Alarmzentrale hat Alarm ausgelöst - Bereich: ' + alarm['BereichsID'] + " - Melder: " + alarm['MelderID'])
       elif benachrichtigungsobj['Typ'] == "Signalgeber_Blitz_Sirene":
         # Signalgeber mit Blitz und Sirene aktivieren
         print("Der Signalgeber mit der ID " + str(benachrichtigungsobj['ID']) + " wird aktiviert!")
         os.system("./modules/alarmsignalgeber.py " + str(benachrichtigungsobj['GPIOBlitz']) + " " + str(benachrichtigungsobj['GPIOSirene']) + " " + str(benachrichtigungsobj['SireneSekunden']) + " &")
       elif benachrichtigungsobj['Typ'] == "Signalgeber_Blitz_Sirene_IP":
         # Signalbeter mit Blitz und Sirene via HTTP/ESP32 aktivieren
         print("Der Signalgeber mit der ID" + str(benachrichtigungsobj['ID']) + " wird aktiviert!")
         os.system("./modules/alarmsignalgeber_esp32.py " + str(benachrichtigungsobj['IP']) + " " + str(benachrichtigungsobj['GPIOBlitz']) + " " + str(benachrichtigungsobj['GPIOSirene']) + " " + str(benachrichtigungsobj['SireneSekunden']) + " &")


      # Markiere den Melder im gemeldeten Bereich als ausgelöst, damit bis zur Quitierung kein erneuter Alarm ausgelöst wird.
      f = open("alarme/aktiv/" + alarm['BereichsID'] + "/" + alarm['MelderID'], "w")
      f.write("1")
      f.close()
      # Die selbe Datei muss im Ordner verleich angelegt werden, damit das Alarmquitierung-Modul nach Quitierung des Alarms die Benachrichtigungen korrekt zurücksetzen kann
      f = open("alarme/vergleich/" + alarm['BereichsID'] + "/" + alarm['MelderID'], "w")
      f.write("1")
      f.close()

  return "ok"
