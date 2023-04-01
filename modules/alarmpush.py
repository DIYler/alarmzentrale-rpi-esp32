#!/usr/bin/python3

import http.client
import urllib.parse

def alarmPush(title, message):
  conn = http.client.HTTPSConnection("GOTIFY_SERVER_URL")
  payload = ''
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }

  titleforurl = urllib.parse.quote(title)
  messageforurl = urllib.parse.quote(message)
  conn.request("POST", "/message?token=GOTIFY_TOKEN&title=" + titleforurl + "&message=" + messageforurl + "&priority=5", payload, headers)
  res = conn.getresponse()
  data = res.read()
  print(data.decode("utf-8"))

  return "alarmpush gesendet"
