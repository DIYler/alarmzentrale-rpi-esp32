#!/usr/bin/python3

### Abfragescript für Melder BWM2: Bewegungsmelder Keller an ESP32 ###

## Dieser Bewegungsmelder ist per GPIO an einem ESP32 angeschlossen bzw. Der ESP32 stellt ein API-Endpoint bereit,
## um den Zustand des GPIO abzufragen
## Informationen zum Abfragen:
##
## API-URL http://192.168.0.102/api/g4
## Wenn der Melder im Normalzustand ist (also nicht meldet), ist der GPIO am ESP32 HIGH. Die API meldet { "GPIO": 4, zustand: 1 }
## Wenn der Melder Alarm meldet, ist der GPIO am ESP32 LOW. Die API meldet { GPIO: 4, zustand: 0 }
##

## Allgemeingültige Regel für alle Melder:
## Melder meldet Alarmzustand -> Abfragescript gibt 1 zurück
## Meldet meldet Normalzustand -> Abfragescript gibt 0 zurück

# Load Libs
import RPi.GPIO as GPIO
import os
import requests
import json
import time as sleep
import modules.melder.loescheStoerung as loescheStoerung
import modules.melder.setzeStoerung as setzeStoerung

def GibZustand():
  # Frage den Melder per API ab
  try:
    response = requests.get('http://192.168.0.102/api/g4', timeout=5)
    zustand = response.json()['zustand']
    # Störung zurücksetzen falls vorhanden
    loescheStoerung.loescheStoerung("BWM2")
  except:
    # Es kann durchaus mal vorkommen, dass der ESP32 nach 5 Sekunden noch nicht bereit ist zum Antworten, probiere erneut
    try:
      sleep.sleep(5) # timeout wartet nur 5 Sekunden, wenn der TCP-Handshake mindestens schon geklappt hat, daher sleep(5) um definitiv 5 Sekunden zu warten
      response = requests.get('http://192.168.0.102/api/g15', timeout=5) 
      zustand = response.json()['zustand']
      # Störung zusrücksetzen falls vorhanden
      loescheStoerung.loescheStoerung("BWM2")
    except:
      # Immer noch kein Lebenszeichen. Störung melden
      setzeStoerung.setzeStoerung("BWM2")
      # Der Melder konnte nicht abgefragt werden. In diesen Fällen wird von einer Störung ausgegangen, es soll kein Alarm ausgelöst werden. deshalb zustand = 1
      zustand = 1

  # WENN zustand == 1, DANN ist alles ok. WENN zustand == 0, DANN ALARM
  if zustand == 1:
    # Normalzustand
    return 0;
  else:
    # Alarmzustand
    return 1;
