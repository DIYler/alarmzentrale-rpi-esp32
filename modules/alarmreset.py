#!/usr/bin/python3

# Dies ist das alarmreset-Modul. Es setzt die zum ausgelösten Bereich in der config.json definierten Benachrichtigungsmittel die deaktiviert werden müssen - 
# dies betrifft insbesondere Blitze oder Leuchten von Signalgebern. Außerdem quitiert dieses Modul Alarme in den Bereichen.

# Die Methode checkReset() wird vom Hauptscript alarmzentrale.py bei jedem Schleifendurchlauf zu jedem Bereich einmal aufgerufen 
# und dabei die BereichID übergeben.

# checkReset() sucht dann dann im Vergelichsordner des Bereichs alarme/vergleich/BereichsID/* nach allen Melderdateien.
# Für jede Melderdatei sucht checkReset() dann zum Vergleich eine passende Melderdatei im Ordner /alarme/aktiv/BereichsID/Melderdatei.
# Wenn Sie nicht mehr existiert oder den Wert 1 enthält, so wurde der Alarm noch nicht quitiert und checkReset() wird nichts unternehmen.
# Existiert die Datei jedoch nicht mehr oder hat den Wert 0, so bedeudet dies, dass der Alarm quitiert wurde. 

# Wurde ein Alarm quitiert, so wird checkReset() alle in der config.json zum quitierten Bereich konfigurierten Benachrichtigungsmittel 
# die zurücksetzt werden müssen, zurücksetzen.

# Anschließend löscht checkReset() alle zum quitierten Bereich gehörenden Melderdatein aus /alarme/vergleich/BereichsID/*
# und /alarme/aktiv/BereichsID/*.

# Wichtig: Wird ein Melder in einem Bereich quitiert, so bewirkt dies, dass der komplette Bereich quitiert wird, auch wenn noch weitere
# Melder in dem Bereich ausgelöst haben sollten, da die Alarm-Benachrichtigungen pro Bereich und nicht pro Melder aktiv sind.

# !!!!! GANZ Wichtig: Es ist möglich, dass das selbe Benachrichtigungsmittel mehreren Bereichen zugeordnet ist.
# Sobald ein Melder in einem Bereich quitiert wird, wo das Benachrichtigungsmittel aktiv war, so wird dieses zurückgesetzt, auch wenn evtl.
# noch unquitierte Alarme in anderen Bereichen vorliegen, wo diese ebenfalls verwendet wird !!!!!

import os
import json
import RPi.GPIO as GPIO
import time as sleep
import requests

# Nummerierung der GPIO-Pins wie auf dem RPi angezeigt verwenden
GPIO.setmode(GPIO.BCM)

# config.json einlesen
configfileobj = open('config/config.json')
config = json.load(configfileobj)
configfileobj.close()

# checkReset
def checkReset(BereichsID):
  # Suche Melderdateien im alarme/vergleich/BereichsID-Ordner
  for f in os.listdir('alarme/vergleich/' + BereichsID):
    quitiert = False
    melderdatei = os.path.join('alarme/vergleich/' + BereichsID, f).replace('alarme/vergleich/' + BereichsID + '/', '')
    # Suche nach der gleichen Melderdatei in alarme/aktiv/BereichsID
    if os.path.exists('alarme/aktiv/' + BereichsID + '/' + melderdatei):
      # Datei gefunden, auslesen und prüfen ob eine 0 (was quitiert bedeutet) drinsteht
      mf = open("alarme/aktiv/" + BereichsID + "/" + melderdatei, "r")
      if int(mf.read()) == 0:
        mf.close()
        # Datei exitiert, hat aber den Wert 0, der Alarm wurde also quitiert!
        print("Melderdatei: " +  'alarme/aktiv/' + BereichsID + '/' + melderdatei + ' hat den Wert 0.')
        quitiert = True
    else:
      # Die Datei existiert nicht, der Alarm wurde also quitiert!
      print("Melderdatei: " +  'alarme/aktiv/' + BereichsID + '/' + melderdatei + ' nicht gefunden.')
      quitiert = True

    # Wurde der Alarm quitiert?
    if quitiert:
      # Der Alarm wurde quitiert! Der Bereich muss zurückgesetzt werden
      # Alle Benachrichtigungsmittel aus der config.json zum quitierten Bereich auslesen und ausschalten
      benachrichtigungen = next(item for item in config['Scharfschaltungsbereiche'] if item["ID"] == BereichsID)["Alarmbenachrichtigungen"]
      for benachrichtigung in benachrichtigungen:
        # Lade Benachrichtigungsobjekt
        benachrichtigungsobj = next(item for item in config['Alarmbenachrichtigung'] if item["ID"] == benachrichtigung)
        print("Die Alarmbenachrichtigung: " + benachrichtigungsobj['ID'] + ' wird zurückgesetzt')

        # Typ: Signalgeber_Blitz_Sirene
        # ACHTUNG! Dieser Block geht von ACTIVE LOW Relays aus, daher GPIO.HIGH zum deaktivieren!
        if benachrichtigungsobj['Typ'] == "Signalgeber_Blitz_Sirene":
          # 1. in der config genannter GPIO
          try: 
            print("Versuche erstes Relay auszuschalten")
            GPIO.output(benachrichtigungsobj['GPIOBlitz'], GPIO.HIGH)
            print("Erstes Relay erfolgreich ausgeschaltet")
          except Exception as e:
            print("fehlgeschlagen, konfiguriere GPIO des ersten Relay als OUT und probiere erneut")
            GPIO.setup(benachrichtigungsobj['GPIOBlitz'], GPIO.OUT)
            GPIO.output(benachrichtigungsobj['GPIOBlitz'],GPIO.HIGH)
            print("Erstes Relay erfolgreich ausgeschaltet")
          # 2. in der config genannter GPIO
          print("Versuche zweites Relay auszuschalten")
          try:
            print("Versuche zweites Relay auszuschalten")
            GPIO.output(benachrichtigungsobj['GPIOSirene'], GPIO.HIGH)
          except Exception as e:
            print("fehlgeschlagen, konfiguriere GPIO des zweiten Relay als OUT und probiere erneut")
            GPIO.setup(benachrichtigungsobj['GPIOSirene'], GPIO.OUT)
            GPIO.output(benachrichtigungsobj['GPIOSirene'],GPIO.HIGH)
            print("Zweites Relay erfolgreich ausgeschaltet")

        # Typ: Signalgeber_Blitz_Sirene_IP
        # ACHTUNG! Dieser Block geht von ACTIVE LOW Relays aus, daher http://IP-ESP32/api/g*/high zum deaktivieren!
        if benachrichtigungsobj['Typ'] == "Signalgeber_Blitz_Sirene_IP":
          # Blitz
          try:
            print("Versuche Blitz auszuschalten")
            response = requests.get('http://' + str(benachrichtigungsobj['IP']) + '/api/g' + str(benachrichtigungsobj['GPIOBlitz']) + '/high', timeout=2)
            print("Blitz erfolgreich ausgeschaltet")
          except Exception as e:
            try:
              print("fehlgeschlagen, probiere Blitz erneut auszuschalten")
              response = requests.get('http://' + str(benachrichtigungsobj['IP']) + '/api/g' + str(benachrichtigungsobj['GPIOBlitz']) + '/high', timeout=2)
              print("Blitz erfolgreich ausgeschaltet")
            except:
              print("Das Ausschalten des Blitz ist erneut fehlgeschlagen! Es wird nicht weiter probiert!")
          # Sirene
          try:
            print("Versuche Sirene auszuschalten")
            response = requests.get('http://' + str(benachrichtigungsobj['IP']) + '/api/g' + str(benachrichtigungsobj['GPIOSirene']) + '/high', timeout=5)
            print("Sirene erfolgreich ausgeschaltet")
          except Exception as e:
            try:
              print("fehlgeschlagen, probiere Sirene erneut auszuschalten")
              response = requests.get('http://' + str(benachrichtigungsobj['IP']) + '/api/g' + str(benachrichtigungsobj['GPIOSirene']) + '/high', timeout=5)
              print("Sirene erfolgreich ausgeschaltet")
            except:
              print("Das Ausschalten der Sirene ist ernuet fehlgeschlagen! Es wird nicht weiter probiert!")


      ##### Hier werden alle Melderdateien aus alarme/vergleich/BereichsID und alarme/aktiv/BereichsID gelöscht #####
      delete_all_files_in_folder('alarme/vergleich/' + BereichsID);
      delete_all_files_in_folder('alarme/aktiv/' + BereichsID);
    return "ok";

	
def delete_all_files_in_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Fehler beim Loeschen einer Melderdatei %s. Grund: %s' % (file_path, e))
