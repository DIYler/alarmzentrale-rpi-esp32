#!/bin/python3

# Dieses Script dient Ansteuern eines Signalgebers mit Blitz und Sirene
# Während der Blitz auf sys.argv[1] dauerhaft aktiviert bleibt, wird die Sirene sys.argv[2] nach einer definierten Zeit 
# in Sekunden sys.argv[3] wieder deaktivert
#
# Dieses Script ist nicht zum Einbinden als Modul in andere Scripte vorgesehen! Es sollte aus anderen Scripten wie folgt aufgerufen werden:
# os.system(./modules/alarmsignalgeber.py 20 21 60) --> Bedeutet beispielsweise Blitz auf GPIO20, Sirene auf GPIO21, Sirene für 60 Sekunden
#
# Achtung! Dieses Script bedient ACTIVE LOW-Relais!!! Deshalb bedeuter GPIO.LOW = Einschalten und GPIO.HIGH = Ausschalten
#

import sys
import RPi.GPIO as GPIO
import time

# Nummerierung der GPIO-Pins wie auf dem RPi angezeigt verwenden
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Blitz aktivieren
GPIO.setup(int(sys.argv[1]), GPIO.OUT)
GPIO.output(int(sys.argv[1]), GPIO.LOW)

# Sirene aktivieren
GPIO.setup(int(sys.argv[2]), GPIO.OUT)
GPIO.output(int(sys.argv[2]), GPIO.LOW)

# In sys.argv[3] definierte Anzahl an Sekunden abwarten
time.sleep(int(sys.argv[3]))

# Sirene deaktivieren
GPIO.output(int(sys.argv[2]),GPIO.HIGH)


