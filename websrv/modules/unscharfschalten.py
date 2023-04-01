#!/bin/python3


import json
from flask import Response

# config.json einlesen
configfileobj = open('config/config.json')
config = json.load(configfileobj)
configfileobj.close()

def unscharfschalten(BereichsID):
  # Bereichsdatei in der Config auf 1 setzencd
  # In config.json prüfen ob der Bereich existiert
  bereichExists = False

  for bereich in config['Scharfschaltungsbereiche']:
    if bereich['ID'] == BereichsID:
      f = open("config/scharfschaltung/" + BereichsID, "w")
      f.write("0")
      f.close()
      bereichExists = True

  if bereichExists:
    return Response(json.dumps({'ergebnis': 'ok', 'text': 'Bereich ' + BereichsID + ' unscharfgeschaltet'}), status=200, mimetype="application/json")

  return Response(json.dumps({'ergebnis': 'fehler', 'text': 'Bereich existiert nicht!'}), status=404, mimetype="application/json")
