#!/bin/python3

import os
import json
from flask import Response

# config.json einlesen
configfileobj = open('config/config.json')
config = json.load(configfileobj)
configfileobj.close()

def getStoerungen():
  gestoerteMelder = [];

  # Prüfen ob Melder mit aktiven Störungen vorliegen
  for f in os.listdir('stoerungen/melder/'):
    print(f)
    stoerungsdatei = os.path.join('stoerungen/melder/', f)
    # Hat Die Störungsdatei den Wert 1?
    print(stoerungsdatei)
    mf = open(stoerungsdatei, "r")
    if int(mf.read()) == 1:
      mf.close()
      # Ein Melder mit einer aktiven Störung liegt vor. Erzeuge ein Dict für die List gestoerteMelder
      gestoerteMelder.append({'melder': f, 'nachricht': 'Der Melder antwortet nicht! Solange die Störung anhält, kann der Melder keinen Alarm auslösen!'})

    # reponse erzeugen
    if gestoerteMelder:
      # Liste der gestörten Melder ausgeben
      return Response(json.dumps({'status': 'stoerung','stoerungen': gestoerteMelder}), status=200, mimetype="application/json")
    else:
      return Response(json.dumps({'status': 'ok', 'nachricht': 'Es liegen keine gestoerten Melder vor.'}), status=200, mimetype="application/json");
