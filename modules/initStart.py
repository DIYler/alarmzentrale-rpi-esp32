#!/usr/bin/python3

# Dies ist das initStart-Modul. Dieses Script wird zum Start der Alarmzentrale aufgerufen.
# Es führt Dinge aus, die helfen, das System auf einen Start-Zustand zu bringen  
import os
import json
import RPi.GPIO as GPIO
import time as sleep

GPIO.setwarnings(False)

# Nummerierung der GPIO-Pins wie auf dem RPi angezeigt verwenden
GPIO.setmode(GPIO.BCM)

# config.json einlesen
configfileobj = open('config/config.json')
config = json.load(configfileobj)
configfileobj.close()

def initStart():
  # GPIO Outs an denen ACTIVE LOW Relays angeschlossen sind, müssen auf HIGH gestellt werden
  # GPIO20
  GPIO.setup(20, GPIO.OUT)
  GPIO.output(20, GPIO.HIGH)
  # GPIO21
  GPIO.setup(21, GPIO.OUT)
  GPIO.output(21, GPIO.HIGH)

  #
  # Hier können bei Bedarf weitere init-Schritte ausgeführt werden
  #
