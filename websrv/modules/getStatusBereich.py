#!/bin/python3

import json
from flask import Response
import modules.scharfschaltung as scharfschaltung

# config.json einlesen
configfileobj = open('config/config.json')
config = json.load(configfileobj)
configfileobj.close()

def getStatusBereich(BereichsID):
  # In config.json prüfen ob der Bereich existiert
  bereichExists = False

  for bereich in config['Scharfschaltungsbereiche']:
    if bereich['ID'] == BereichsID:
      bereichExists = True

  if bereichExists:
    # Abfragen ob der Bereich Scharf- oder Unscharf geschaltet ist
    if scharfschaltung.isBereichScharf(BereichsID):
      # Der Bereich ist scharf
      return Response(json.dumps({'ergebnis': 'ok', 'bereich': BereichsID, 'status': 'scharf'}), status=200, mimetype="application/json")
    else:
      # Der Bereich ist unscharf
      return Response(json.dumps({'ergebnis': 'ok', 'bereich': BereichsID, 'status': 'unscharf'}), status=200, mimetype="application/json") 

  return Response(json.dumps({'ergebnis': 'fehler', 'text': 'Bereich existiert nicht!'}), status=404, mimetype="application/json")
