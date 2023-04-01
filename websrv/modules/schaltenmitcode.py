#!/bin/python3

import os
import json
from flask import Response

# Module zum Abfragen der Scharfschaltung eines Bereichs
import modules.scharfschaltung as scharfschaltung

# Melderabfrage
import modules.melderabfrage as melderabfrage

# config.json einlesen
configfileobj = open('config/config.json')
config = json.load(configfileobj)
configfileobj.close()

def schaltenmitcode(Code):
  # Codeliste

  if Code == "1234A":
    # Code zum Scharfschalten des Bereich HausExtern
    BereichsID = "HausExtern"
    return scharfschalten(BereichsID)
  elif Code == "1234AA":
    # Code zum Unscharfschalten des Bereich HausExtern
    BereichsID = "HausExtern"
    return unscharfschalten(BereichsID)
  elif Code == "1234AAA":
    # Code zum quitieren des Bereich HausExtern
    BereichsID = "HausExtern"
    return alarmquitieren(BereichsID)
  elif Code == "1234AAAA":
    # Code zum Abfragen des Bereich HausExtern
    BereichsID = "HausExtern"
    return getStatusBereich(BereichsID)


  elif Code == "1234B":
    # Code zum Scharfschalten des Bereich HausIntern
    BereichsID = "HausIntern"
    return scharfschalten(BereichsID)
  elif Code == "1234BB":
    # Code zum Unscharfschalten des Bereich HausIntern
    BereichsID = "HausIntern"
    return unscharfschalten(BereichsID)
  elif Code == "1234BBB":
    # Code zum Unscharfschalten des Bereich HausIntern
    BereichsID = "HausIntern"
    return alarmquitieren(BereichsID)
  elif Code == "1234BBBB":
    # Code zum Abfragen des Bereich HausIntern
    BereichsID = "HausIntern"
    return getStatusBereich(BereichsID)

  if Code == "1234A":
    # Code zum Scharfschalten des Bereich HausExtern
    BereichsID = "HausExtern"
    return scharfschalten(BereichsID)
  elif Code == "1234AA":
    # Code zum Unscharfschalten des Bereich HausExtern
    BereichsID = "HausExtern"
    return unscharfschalten(BereichsID)
  elif Code == "1234AAA":
    # Code zum quitieren des Bereich HausExtern
    BereichsID = "HausExtern"
    return alarmquitieren(BereichsID)
  elif Code == "1234AAAA":
    # Code zum quitieren des Bereich HausExtern
    BereichsID = "HausExtern"
    return getStatusBereich(BereichsID)

  else:
    return Response("Der eingegebene Code ist ungueltig!", status=200, mimetype="text/plain")


def scharfschalten(BereichsID):
  bereichExists = False
  nichtBereiteMelder = ""

  # In config.json prüfen ob der Bereich existiert
  for bereich in config['Scharfschaltungsbereiche']:
    if bereich['ID'] == BereichsID:
      # Bereich in config.json gefunden
      # Prüfe, ob alle dem Bereich zugeordneten Melder keinen Alarm melden
      for melder in bereich['Melder']:
        # Frage den aktuellen Zustand des Melders ab
        if melderabfrage.isMelderstatusAlarm(melder):
          # Melder meldet ALARM!!! Der Bereich darf noch nicht scharfgeschaltet werden
          # alarme.append({"MelderID": melder})
          nichtBereiteMelder += melder + ", "

      if nichtBereiteMelder == "":
        # Alle Melder sind Bereit, Bereich scharfschalten
        f = open("config/scharfschaltung/" + BereichsID, "w")
        f.write("1")
        f.close()

      bereichExists = True

  if nichtBereiteMelder != "":
    # Nicht alle Melder sind bereit!
    return Response('Der Bereich ' + BereichsID + ' kann noch nicht scharfgeschaltet werden, da folgende Melder gerade ausloesen: ' + nichtBereiteMelder, status=200, mimetype="text/plain")

  if bereichExists:
    # Alles Ok, der Bereich wurde scharfgeschaltet
    return Response('Der Bereich ' + BereichsID + ' wurde erfolgreich SCHARF geschaltet!', status=200, mimetype="text/plain")


  # Bereich existiert nicht
  return Response('Der zum eingegebenen Code hinterlegte Bereich ' + BereichsID + ' existiert nicht!', status=200, mimetype="text/plain")


def unscharfschalten(BereichsID):
  bereichExists = False

  # Bereichsdatei auf 0 setzen
  for bereich in config['Scharfschaltungsbereiche']:
    if bereich['ID'] == BereichsID:
      f = open("config/scharfschaltung/" + BereichsID, "w")
      f.write("0")
      f.close()
      bereichExists = True

  if bereichExists:
    return Response('Bereich ' + BereichsID + ' UNSCHARF geschaltet!', status=200, mimetype="text/plain")

  return Response('Der zum eingegebenen Code hinterlege Bereich ' + BereichsID + ' existiert nicht!', status=200, mimetype="text/plain")





def alarmquitieren(BereichsID):
  # In config.json prüfen ob der Bereich existiert
  bereichExists = False

  for bereich in config['Scharfschaltungsbereiche']:
    if bereich['ID'] == BereichsID:
      bereichExists = True

  if bereichExists:
    # Alarme des Bereichs löschen. Hinweis: Es genügt den Alarm eines ausgelösten Melders aus dem Bereich zu löschen.
    # Die Alarmzentrale löscht dann selbständig auch Alarme weiterer Melder des selben Bereichs und setzt die zum Bereich eingestellten Signalgeber zurück.
    delete_first_file_in_folder('alarme/aktiv/' + BereichsID)
    return Response('Alarme im Bereich ' + BereichsID + ' quitiert.', status=200, mimetype="text/plain")

  return Response('Der zum eingegebenen Code hinterlege Bereich ' + BereichsID + ' existiert nicht!', status=200, mimetype="text/plain")


def delete_first_file_in_folder(folder):
  isFirst = True
  for filename in os.listdir(folder):
      if isFirst:
        isFirst = False
        # Erste Datei
        file_path = os.path.join(folder, filename)
        try:
          if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
          elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
        except Exception as e:
          print('Failed to delete %s. Reason: %s' % (file_path, e))




def getStatusBereich(BereichsID):
  bereichExists = False

  # In config.json prüfen, ob der Bereich existiert
  for bereich in config['Scharfschaltungsbereiche']:
    if bereich['ID'] == BereichsID:
      bereichExists = True

  if bereichExists:
    # Abfragen ob der Bereich Scharf- oder Unscharf geschaltet ist
    if scharfschaltung.isBereichScharf(BereichsID):
      # Der Bereich ist scharf
      return Response('Der Bereich ' + BereichsID + ' ist SCHARF!!!', status=200, mimetype="text/plain")
    else:
      # Der Bereich ist unscharf
      return Response('Der Bereich ' + BereichsID + ' ist UNSCHARF.', status=200, mimetype="text/plain")

  return Response('Der zum eingegebenen Code hinterlegte Bereich ' + BereichsID + ' existiert nicht!', status=200, mimetype="text/plain")
