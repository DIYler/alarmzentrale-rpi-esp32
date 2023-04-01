#!/bin/python3

import json
from flask import Response

# Melderabfrage
import modules.melderabfrage as melderabfrage

# config.json einlesen
configfileobj = open('config/config.json')
config = json.load(configfileobj)
configfileobj.close()

def scharfschalten(BereichsID):
  bereichExists = False
  nichtBereiteMelder = ""

  # In config.json prüfen ob der Bereich existiert
  for bereich in config['Scharfschaltungsbereiche']:
    if bereich['ID'] == BereichsID:
      # Bereich in config.json gefunden
      # Prüfe, ob alle dem Bereich zugeordneten Melder keinen Alarm melden
      for melder in bereich['Melder']:
        # Frage den aktuellen Zustand des Melders ab
        if melderabfrage.isMelderstatusAlarm(melder):
          # Melder meldet ALARM!!! Der Bereich darf noch nicht scharfgeschaltet werden
          # alarme.append({"MelderID": melder})
          nichtBereiteMelder += melder + ", "

      if nichtBereiteMelder == "":
        # Alle Melder sind Bereit, Bereich scharfschalten
        f = open("config/scharfschaltung/" + BereichsID, "w")
        f.write("1")
        f.close()

      bereichExists = True

  if nichtBereiteMelder != "":
    # Nicht alle Melder sind bereit!
      return Response(json.dumps({'ergebnis': 'fehler', 'text': 'Der Bereich ' + BereichsID + ' kann noch nicht scharfgeschaltet werden, da folgende Melder gerade auslösen: ' + nichtBereiteMelder}), status=403, mimetype="application/json")

  if bereichExists:
    # Alles Ok, der Bereich wurde scharfgeschaltet
    return Response(json.dumps({'ergebnis': 'ok', 'text': 'Bereich ' + BereichsID + ' scharfgeschaltet'}), status=200, mimetype="application/json")


  # Bereich existiert nicht
  return Response(json.dumps({'ergebnis': 'fehler', 'text': 'Bereich existiert nicht!'}), status=404, mimetype="application/json")
