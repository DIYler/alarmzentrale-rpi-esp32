#!/usr/bin/python3

### Abfragescript für Melder DominikWohnzimmerTuer: Türkontakt Dominik Wohnzimmer Tür ###

## Dieser Türkontakt bzw. Reed-Schalter ist NC. 
## Ist die Tür zu, ist der Schalter geschlossen - Strom fließt - GPIO registiert ein HIGH
## Ist die Tür auf, ist der Schalter geöffnet - Strom fließt nicht - GPIO registriert ein LOW

## Allgemeingültige Regel für alle Melder:
## Melder meldet Alarmzustand -> Abfragescript gibt 1 zurück
## Meldet meldet Normalzustand -> Abfragescript gibt 0 zurück

# Load Libs
import RPi.GPIO as GPIO

def GibZustand():
  # Melder DominikWohnzimmerTuer liegt auf GPIO4
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

  # WENN GPIO4 HIGH, DANN ist alles ok. WENN GPIO4 LOW, DANN ALARM
  if GPIO.input(4) == 1:
    # Normalzustand
    return 0;
  else:
    # Alarmzustand
    return 1;
