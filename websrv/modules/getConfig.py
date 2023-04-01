#!/bin/python3

# REST-API Service, der bestimmte Bereiche aus der config.json ausspuckt

import json
from flask import Response

# Melderabfrage
import modules.melderabfrage as melderabfrage

# config.json einlesen
configfileobj = open('config/config.json')
config = json.load(configfileobj)
configfileobj.close()

def getBereiche():
  # Gibt die Scharfschaltungbereiche aus der config-zurück
  return Response(json.dumps(config['Scharfschaltungsbereiche']), status=200, mimetype="application/json")
