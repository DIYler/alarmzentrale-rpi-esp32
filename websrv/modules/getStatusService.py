#!/bin/python3

import json
import os
from flask import Response

# Melderabfrage
#import modules.melderabfrage as melderabfrage

# config.json einlesen
configfileobj = open('config/config.json')
config = json.load(configfileobj)
configfileobj.close()

def getStatusService():
  # Gibt per JSON eine Antwort zurück, ob der systemctl-service "Alarmzentrale" active oder inactive ist
  statusstream = os.popen('systemctl is-active alarmzentrale')
  status = statusstream.read()
  dict = {}
  dict['service'] = 'alarmzentrale'
  dict['status'] = status.replace("\n","")
  return Response(json.dumps(dict), status=200, mimetype="application/json")
