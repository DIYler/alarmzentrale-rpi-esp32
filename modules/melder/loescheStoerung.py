#!/bin/python3

import os
import modules.alarmpush as alarmpush
import modules.alarmpushover as alarmpushover

def loescheStoerung(MelderID):
  # Der Melder antwortet. Prüfe ob es eine aktive Störung gibt und setze diese zurück
  if os.path.exists('stoerungen/melder/' + MelderID):
    f = open('stoerungen/melder/' + MelderID, 'r')
    if int(f.read()) == 1:
      f.close()
      # Es liegt eine aktive Störung für diesen Melder vor. Melden, dass der Melder wieder reagiert
      print("!!!HINWEIS!!! - Melder " + MelderID + " antworter wieder!")
      alarmpush.alarmPush("!!!HINWEIS!!! - Melder: " + MelderID, "!!!HINWEIS!!! - Melder: " + MelderID + " antwortet wieder. Die Störung wird gelöscht und der Melder ist wieder einsatzbereit!")
      alarmpushover.alarmPushover("ue4jq7dgha9wxgq1reij922a6mk6zc","!!!HINWEIS!!! - Melder: " + MelderID,'<font color="orange">!!!HINWEIS!!!</font> - Melder: ' + MelderID + ' antwortet wieder. Die Störung wird gelöscht und der Melder ist wieder einsatzbereit!')
      # Setze Störungsdatei des Melders auf 0
      f = open('stoerungen/melder/' + MelderID, 'w')
      f.write("0")
      f.close()
