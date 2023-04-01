#!/usr/bin/python3

### Abfragescript für Melder BWM1: Bewegungsmelder Flur an RPi ###

## Dieser Bewegungsmelder ist NC.
## Wenn keine Bewegung, ist der Schalter geschlossen - Strom fließt - GPIO registiert ein HIGH
## Wenn Bewegung, ist der Schalter geöffnet - Strom fließt nicht - GPIO registriert ein LOW

## Allgemeingültige Regel für alle Melder:
## Melder meldet Alarmzustand -> Abfragescript gibt 1 zurück
## Meldet meldet Normalzustand -> Abfragescript gibt 0 zurück

# Load Libs
import RPi.GPIO as GPIO

def GibZustand():
  # Melder BWM1 liegt auf GPIO5
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

  # WENN GPIO5 HIGH, DANN ist alles ok. WENN GPIO22 LOW, DANN ALARM
  if GPIO.input(5) == 1:
    # Normalzustand
    return 0;
  else:
    # Alarmzustand
    return 1;
