#!/bin/python3

import os
import json
from flask import Response

# config.json einlesen
configfileobj = open('config/config.json')
config = json.load(configfileobj)
configfileobj.close()

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
    return Response(json.dumps({'ergebnis': 'ok', 'text': 'Alarme für den Bereich ' + BereichsID + ' wurden quitiert'}), status=200, mimetype="application/json") 

  return Response(json.dumps({'ergebnis': 'fehler', 'text': 'Bereich existiert nicht!'}), status=404, mimetype="application/json")



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
