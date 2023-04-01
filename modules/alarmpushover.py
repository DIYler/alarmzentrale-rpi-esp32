#!/usr/bin/python3

import http.client
import requests
import urllib.parse
import shutil

# Push-Nachricht an Pushover-Client senden
# Diese Methode übermittelt auch ein aktuelles Bild einer IP-Überwachungskamera 
def alarmPushover(userkey, title, message):
  downloadPictureFromCam()
  r = requests.post("https://api.pushover.net/1/messages.json", data = {
    "token": "PUSHOVER_APPLICATION_TOKEN",
    "user": userkey,
    "title": title,
    "message": message,
    "sound": "siren",
    "html": "1",
    "priority": "1"
  },
  files = {
    "attachment": ("image.jpeg", open("temp/door.jpeg", "rb"), "image/jpeg")
  })
  print(r.text)


def downloadPictureFromCam():
  url = "http://IP-CAM/PATH_TO_JPEG"
  file = "temp/door.jpeg"

  try:
    res = requests.get(url, stream = True, timeout=2)
    if res.status_code == 200:
      with open(file,'wb') as f:
        shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ',file)
        f.close()
    else:
      print('Image Couldn\'t be retrieved')
  except:
    print('Kamera nicht erreichbar - Pushover wird ohne aktuelles Bild versandt')
