#!/bin/python3

import os
import json
from flask import Response
import modules.scharfschaltung as scharfschaltung

# config.json einlesen
configfileobj = open('config/config.json')
config = json.load(configfileobj)
configfileobj.close()

def getUnquitierteAlarme(BereichsID):
  # In config.json prüfen ob der Bereich existiert
  bereichExists = False

  for bereich in config['Scharfschaltungsbereiche']:
    if bereich['ID'] == BereichsID:
      bereichExists = True

  if bereichExists:
    # Abfragen ob unquitierte Alarme für diesen Bereich vorliegen
    # Unquitierte Alarme liegen vor, wenn Melderdateien im Ordner alarme/aktiv/DominikVoll existieren und diese den Wert 1 enhalten

    unquitierteAlarme = [];

    # Suche Melderdateien im alarme/vergleich/BereichsID-Ordner
    for f in os.listdir('alarme/aktiv/' + BereichsID):
      quitiert = False
      melderdatei = os.path.join('alarme/aktiv/' + BereichsID, f).replace('alarme/aktiv/' + BereichsID + '/', '')
      # Hat die Melderdatei den Wert 1?
      mf = open("alarme/aktiv/" + BereichsID + "/" + melderdatei, "r")
      if int(mf.read()) == 1:
       mf.close()
       # Dies ist ein unquitierter, also noch aktiver Alarm. Schreibe ein dict mit dem Melder(datei) in die list unquitierteAlarme  
       unquitierteAlarme.append(melderdatei)

    # Befinden sich Einträge in der Liste? Wenn ja liegen unquitierte aktive Alarme vor
    if unquitierteAlarme:
      # Die Liste ist nicht leer. Erzeuge die Response
      return Response(json.dumps({'ergebnis': 'ok', 'bereich': BereichsID, 'status': 'alarm', 'melder': unquitierteAlarme}), status=200, mimetype="application/json")

    # Alles gut, es liegen keine unquitierten Alarme vor. Erzeuge die Response
    return Response(json.dumps({'ergebnis': 'ok', 'bereich': BereichsID, 'status': 'sicher'}), status=200, mimetype="application/json")

  return Response(json.dumps({'ergebnis': 'fehler', 'text': 'Bereich existiert nicht!'}), status=404, mimetype="application/json")
