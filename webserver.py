#!/bin/python
# Dies ist der Webserver der Alarmzentrale. Er ist von der Kernlogik der Alarmzentrale völlig losgelöst und hat primär die Aufgabe
# eine HTTP-&-REST-Schnittstelle für die Bedienung der Alarmzentrale zur Verfügung zu stellen. Außerdem stellt er selber via HTTP
# eine einfache Webseite zur Steuerung bereit.

import websrv.modules.scharfschalten as scharfschalten
import websrv.modules.unscharfschalten as unscharfschalten
import websrv.modules.schaltenmitcode as schaltenmitcode
import websrv.modules.getStatusBereich as getStatusBereich
import websrv.modules.getStoerungen as getStoerungen
import websrv.modules.alarmquitieren as alarmquitieren
import websrv.modules.getUnquitierteAlarme as getUnquitierteAlarme
import websrv.modules.getStatusService as getStatusService
import websrv.modules.startService as startService

import websrv.modules.getConfig as getConfig

from flask import Flask,request
from flask import send_from_directory

app = Flask(__name__,static_folder="websrv")

@app.route('/')
def hello_world():
    return app.send_static_file('html/home.html')
    #return '<html><title>Alarmzentrale</title><body style="font-family:roboto"><h1>Willkommen auf der Alarmzentrale</h1></body></html>'

@app.route('/icons/android-chrome-192x192.png')
def icon1():
    return app.send_static_file('html/icons/android-chrome-192x192.png')

@app.route('/icons/android-chrome-512x512.png')
def icon2():
    return app.send_static_file('html/icons/android-chrome-512x512.png')

@app.route('/icons/apple-touch-icon.png')
def icon3():
    return app.send_static_file('html/icons/apple-touch-icon.png')

@app.route('/icons/favicon-16x16.png')
def icon4():
    return app.send_static_file('html/icons/favicon-16x16.png')

@app.route('/icons/favicon-32x32.png')
def icon5():
    return app.send_static_file('html/icons/favicon-32x32.png')

@app.route('/icons/favicon.ico')
def icon6():
    return app.send_static_file('html/icons/favicon.ico')

@app.route('/icons/site.webmanifest')
def icon7():
    return app.send_static_file('html/icons/site.webmanifest')

@app.route('/js/alarmzentrale_api.js')
def jsAlarmzentraleAPI():
  return app.send_static_file('js/alarmzentrale_api.js')


# ----------- Beginn der API-Endpoints ----------

@app.route('/api/scharfschalten')
def callScharfschalten():
  bereich = request.args.get('bereich')
  return scharfschalten.scharfschalten(bereich)

@app.route('/api/unscharfschalten')
def callUnscharfschalten():
  bereich = request.args.get('bereich')
  return unscharfschalten.unscharfschalten(bereich)

@app.route('/api/schaltenmitcode')
def callSchaltenmitcode():
  code = request.args.get('code')
  return schaltenmitcode.schaltenmitcode(code)

@app.route('/api/alarmquitieren')
def callAlarmQuitieren():
  bereich = request.args.get('bereich')
  return alarmquitieren.alarmquitieren(bereich)

@app.route('/api/getunquitiertealarme')
def callGetUnquitierteAlarme():
  bereich = request.args.get('bereich')
  return getUnquitierteAlarme.getUnquitierteAlarme(bereich)

@app.route('/api/getstatusbereich')
def callGetStatusBereich():
  bereich = request.args.get('bereich')
  return getStatusBereich.getStatusBereich(bereich)

@app.route('/api/getBereiche')
def callGetBereiche():
  return getConfig.getBereiche()

@app.route('/api/getstoerungen')
def callGetStoerungen():
  return getStoerungen.getStoerungen()

@app.route('/api/getstatusservice')
def callGetStatusService():
  return getStatusService.getStatusService()

@app.route('/api/startservice')
def callStartService():
  return startService.startService()

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
