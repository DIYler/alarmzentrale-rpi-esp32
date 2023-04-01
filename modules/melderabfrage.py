#!/usr/bin/python3


# Script zum Abfragen aller Melder, welche durch die Alarmzentrale überwacht werden
#
# Jeder Melder der überwacht werden soll, benötigt ein eigenes Abfragescript, um dessen Status abzufragen.
# Das Abfragescript muss anschließend hier als Modul importiert werden und in der Methode isMelderstatusAlarm() im if aufgerufen werden
# Dadurch wird der Melder der Alarmzentrale bekannt gemacht und kann durch sie abgefragt werden
#
# Für alle Abfragescripte gelten folgende einheitliche Regeln:
# 1. Alle Abfragescripte haben eine Methode GibZustand()
# 2. Meldet der Melder Alarm, so muss GibZustand() = True zurückgeben
# 3. Meldet der Melder keinen Alarm, so muss GibZustand() = False zurückgeben
#
# Durch diese einheitlichen Regeln ist es der Alarmzentrale völlig egal um was für eine Art von Melder es sich handelt.
# Egal ob Kabelgebunden, Funkgebunden, ob Reed-Kontakte, Bewegungsmelder, Wassermelder, Temperatursensoren, usw...
# Egal ob direkt am RPi angeschlossen oder an einem anderen Gerät wie einem ESP32 mit abfragbarer Schnittstelle
# Alle Meöder können so einheitlich abgefragt wird. Wie geanu ein bestimmeter Melder/Sensor abgefragt wird, ob es sich um ein NC oder NO handelt,
# und weitere Melder/Sensor bezifische Details wie zum Beispiel Schwellwerte, werden vom Abfragescript des Melders entschieden. 


# Melderabfrage-Module
import modules.melder.Tuer1 as Tuer1
import modules.melder.Tuer2 as Tuer2
import modules.melder.Fenster1 as Fenster1
import modules.melder.Fenster2 as Fenster2
import modules.melder.BWM1 as BWM1
import modules.melder.BWM2 as BWM2

def isMelderstatusAlarm(MelderID):
  isAlarm = False

  # Melder abfragen 
  if MelderID == "Tuer1":
    isAlarm = Tuer1.GibZustand()
  elif MelderID == "Tuer2":
    isAlarm = Tuer2.GibZustand()
  elif MelderID == "Fenster1":
    isAlarm = Fenster1.GibZustand()
  elif MelderID == "Fenster2":
    isAlarm = Fenster2.GibZustand()
  elif MelderID == "BWM1":
    isAlarm = BWM1.GibZustand()
  elif MelderID == "BWM2":
    isAlarm = BWM2.GibZustand()
  else:
    raise Exception("Der Melder mit der MelderID: " + MelderID + " ist dem Melderabfrage-Module nicht bekannt!")

  return isAlarm
