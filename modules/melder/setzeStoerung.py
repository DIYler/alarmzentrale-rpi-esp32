#!/bin/python3

import os
import modules.alarmpush as alarmpush
import modules.alarmpushover as alarmpushover

def setzeStoerung(MelderID):
  # Prüfe ob bereits eine Störung für diesen Melder gemeldet wurde. Wenn nicht, melden
  if not os.path.exists('stoerungen/melder/' + MelderID):
    # Störungsdatei existiert für den Melder noch nicht. Lege Störungsdatei an und setze Wert auf 0
    f = open('stoerungen/melder/' + MelderID, 'w')
    f.write("0")
    f.close()
  # Prüfe ob für diesen Melder bereits eine Störung gemeldet wurde
  f = open('stoerungen/melder/' + MelderID, "r")
  if int(f.read()) == 0:
    f.close()
    # Störung noch nicht gemeldet. Störung jetzt melden
    print("!!!STÖRUNG!!! - Melder " + MelderID + " antwortet nicht!")
    alarmpush.alarmPush("!!!STÖRUNG!!! - Melder: " + MelderID, "!!!STÖRUNG!!! - Melder: " + MelderID + " hat zum wiederholten Male nicht geantwortet! Dies wird sehr wahrscheinlich auf ein unbeabsichtigtes technisches Problem zurückzuführen sein, in unwahrscheinlichen Fällen könnte aber auch eine bewusste Manipulation des WLAN-Signals oder der Stromversorgung die Ursache dafür sein! Da ein technisches Problem am wahrscheinlichsten ist, löst die Alarmzentrale keinen Alarm aus. Solange der Melder im Störungsmodus ist, kann er keinen Alarm melden!")
    alarmpushover.alarmPushover("PUSHOVER_USERKEY","!!!STÖRUNG!!! - Melder: " + MelderID,'<font color="orange">!!!STÖRUNG!!!</font> - Melder: ' + MelderID + ' hat zum wiederholten Male nicht geantwortet! Dies wird sehr wahrscheinlich auf ein unbeabsichtigtes technisches Problem zurückzuführen sein, in unwahrscheinlichen Fällen könnte aber auch  eine bewusste Manipulation des WLAN-Signals oder der Stromversorgung die Ursache dafür sein! Da ein technisches Problem am wahrscheinlichsten ist, löst die Alarmzentrale keinen Alarm aus. Solange der Melder im Störungsmodus ist, kann er keinen Alarm melden!');
    # Setze Störungsdatei des Melders auf 1
    f = open('stoerungen/melder/' + MelderID, 'w')
    f.write("1")
    f.close()
