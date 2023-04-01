#!/usr/bin/python3

def isBereichScharf(ScharfschaltungsbereichID):
  status = False

  ladestatusbereich = open('config/scharfschaltung/' + ScharfschaltungsbereichID)
  lesestatusbereich = ladestatusbereich.read()

  if int(lesestatusbereich) == 1:
    status = True

  ladestatusbereich.close()

  return status
