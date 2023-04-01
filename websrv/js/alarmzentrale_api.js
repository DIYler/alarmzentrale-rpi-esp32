      let isScharfchaltenButtonClicked = false;
      let isUnscharfchaltenButtonClicked = false;
      let isAlarmequitierenButtonClicked = false;

      async function getDienst() {
        const response = await fetch('/api/getstatusservice');
        const dienst = await response.json();

        //Lade Tabelle
        var table = document.getElementById("dienst");

        //Table-Header
        var row1 = table.insertRow();
        row1.insertCell().innerHTML = "<b>Service</b>";
        row1.insertCell().innerHTML = "<b>Status</b>";

        //Dienststatus-Zeile
        row = table.insertRow();
        row.insertCell().innerHTML = dienst.service;

        if(dienst.status === 'active') {
          row.insertCell().innerHTML = '<span style="color: green;">' + dienst.status + '</span>';
        } else if(dienst.status === 'inactive') {
          row.insertCell().innerHTML = '<span style="color: red;">' + dienst.status + '</span>'
          row1.insertCell().innerHTML = "<b>Service starten</b>";
          row.insertCell().innerHTML = '<a id="startenlink" href="#" onclick="dienstStarten()"><b>Hier klicken um den Dienst zu starten</b></a>'; 
        } else { 
          row.insertCell().innerHTML = '<span style="color: orange;">unbekannt</span>'
        }
      }

      async function dienstStarten() {
        const response = await fetch('/api/startservice');
        // Bisherige Tabelle löschen
        let table = document.getElementById("dienst");
        for(let i = table.rows.length - 1; i >= 0; i--) {
         table.deleteRow(i);
        }

        //Dienststatus-Tabelle neu laden
        getDienst();
      }

      async function getStoerungen() {
        const response = await fetch('/api/getstoerungen');
        const stoerungen = await response.json();

        let hstoerungen = document.getElementById("HStoerungen");
        let table = document.getElementById("stoerungen");
        //Response auf Störungen prüfen
        if(stoerungen.status === "stoerung") {
          //Es liegen Störungen vor.
          //Überschrift aktivieren
          hstoerungen.innerHTML = 'Störungen';
          hstoerungen.style.marginTop = '50px';
          //Tabelle erzeugen
          //Table-Header
          var row = table.insertRow();
          row.insertCell().innerHTML = "<b>Melder</b>";
          row.insertCell().innerHTML = "<b>Störungsmeldung</b>";
          stoerungen.stoerungen.forEach(function(stoerung) {
            //Tabelle neue Zeile
            row = table.insertRow();
            row.insertCell().innerHTML = stoerung.melder;
            row.insertCell().innerHTML = '<span style="color: red;">' + stoerung.nachricht + '</span>';
         });
        }
      }

      async function getBereiche() {
        const response = await fetch('/api/getBereiche');
        const bereiche = await response.json();

        console.log(bereiche);

        //Lade Tabelle
        var table = document.getElementById("alleBereiche");

        //Table-Header
        var row = table.insertRow();
        row.insertCell().innerHTML = "<b>Bereich</b>";
        row.insertCell().innerHTML = "<b>Status</b>";
        row.insertCell().innerHTML = "<b>Alarmstatus</b>";
        row.insertCell().innerHTML = "<b>Beschreibung</b>";

        bereiche.forEach(async function(bereich) {
          //Für jeden Bereich abfragen, ob er scharf oder unscharf ist
          console.log(bereich)
          const callgetstatusbereich =  await fetch('/api/getstatusbereich?bereich=' + bereich.ID);
          const statusbereich = await callgetstatusbereich.json();

          var row = table.insertRow();
          row.insertCell().innerHTML = bereich.ID;

          if(callgetstatusbereich.status === 200) {
            if(statusbereich.status === "scharf") {
             row.insertCell().innerHTML = '<span style="color: red;">' + statusbereich.status; + '</span>';
            } else {
             row.insertCell().innerHTML = '<span style="color: green;">' + statusbereich.status; + '</span>';
            } 
          } else {
             row.insertCell().innerHTML = '<span style="color: yellow;">unbekannt</span>';
          }

          //Für jeden Bereich abfragen, ob Alarme vorliegen
          const callgetunquitiertealarme =  await fetch('/api/getunquitiertealarme?bereich=' + bereich.ID);
          const statusalarme = await callgetunquitiertealarme.json();
          if(callgetunquitiertealarme.status === 200) {
            if(statusalarme.status === "alarm") {
             row.insertCell().innerHTML = '<span style="color: red;">' + statusalarme.status + '</span>';
            } else {
             row.insertCell().innerHTML = '<span style="color: green;">' + statusalarme.status; + '</span>';
            }
          } else {
             row.insertCell().innerHTML = '<span style="color: yellow;">unbekannt</span>';
          }



          row.insertCell().innerHTML = bereich.Bezeichnung;
        });
      }

      async function renewGetBereiche() {
       // Bisherige Tabelle löschen
       let table = document.getElementById("alleBereiche");
       for(let i = table.rows.length - 1; i >= 0; i--) {
         table.deleteRow(i);
       }
       //Tabelle neu laden
       getBereiche();
      }

      async function getBereichzumScharfschalten() {
        const response = await fetch('/api/getBereiche');
        const bereiche = await response.json();

        //Lade Bereiche in Tabelle
        var table = document.getElementById("tableScharfschalten");

        console.log(document.getElementsByClassName("buttonBereichScharfschalten"));
        if(!isScharfchaltenButtonClicked) {
          isScharfchaltenButtonClicked = true;
          bereiche.forEach(function(bereich) {
            //Für jeden Bereich eine Zeile
            var row = table.insertRow();
            row.insertCell().innerHTML = '<button type="button" class="btn btn-secondary mg-t-20" onclick="bereichScharfschalten(\'' + bereich.ID + '\')">Bereich <b>' + bereich.ID + '</b> scharfschalten</button><br><span id="scharfschalten_' + bereich.ID + '"></span>';
          });
        } else {
          for(let i = table.rows.length - 1; i >= 0; i--) {
            table.deleteRow(i);
          }
          isScharfchaltenButtonClicked = false;
        }
        //Die Tabelle in der Uebersicht aktuallisieren
        renewGetBereiche();
      }

      async function bereichScharfschalten(bereich) {
        const response = await fetch('/api/scharfschalten?bereich=' + bereich);
        const responseobj = await response.json();
        if(response.status === 200) {
          let p = document.getElementById("scharfschalten_" + bereich);
          p.innerHTML = '<span style="color: green; font-weight: bold;">' + responseobj.text + '</span>';
        } else {
          let p = document.getElementById("scharfschalten_" + bereich);
          p.innerHTML = '<span style="color: red; font-weight: bold;">' + responseobj.text + '</span>';
        }

        //Die Tabelle in der Uebersicht aktuallisieren
        renewGetBereiche();
      }


      async function getBereichzumUnscharfschalten() {
        const response = await fetch('/api/getBereiche');
        const bereiche = await response.json();

        //Lade Bereiche in Tabelle
        var table = document.getElementById("tableUnscharfschalten");

        if(!isScharfchaltenButtonClicked) {
         isScharfchaltenButtonClicked = true; 
         bereiche.forEach(function(bereich) {
            //Für jeden Bereich eine Zeile
            var row = table.insertRow();
            row.insertCell().innerHTML = '<button type="button" class="btn btn-secondary mg-t-20" onclick="bereichUnscharfschalten(\'' + bereich.ID + '\')">Bereich <b>' + bereich.ID + '</b> unscharfschalten</button><br><span id="unscharfschalten_' + bereich.ID + '"></span>';
          });
        } else {
          for(let i = table.rows.length - 1; i >= 0; i--) {
            table.deleteRow(i);
          }
          isScharfchaltenButtonClicked = false;
        }
      }

      async function bereichUnscharfschalten(bereich) {
        const response = await fetch('/api/unscharfschalten?bereich=' + bereich);
        const responseobj = await response.json();
        if(response.status === 200) {
          let p = document.getElementById("unscharfschalten_" + bereich);
          p.innerHTML = '<span style="color: green; font-weight: bold;">' + responseobj.text + '</span>';
        } else {
          let p = document.getElementById("unscharfschalten_" + bereich);
          p.innerHTML = '<span style="color: red; font-weight: bold;">' + responseobj.text + '</span>';
        }

        //Die Tabelle in der Uebersicht aktuallisieren
        renewGetBereiche();
      }


      async function getBereichzumAlarmquitieren() {
        const response = await fetch('/api/getBereiche');
        const bereiche = await response.json();

        //Lade Bereiche in Tabelle
        var table = document.getElementById("tableAlarmquitieren");

        if(!isAlarmequitierenButtonClicked) {
          isAlarmequitierenButtonClicked = true;
          bereiche.forEach(function(bereich) {
            //Für jeden Bereich eine Zeile
            var row = table.insertRow();
            row.insertCell().innerHTML = '<button type="button" class="btn btn-secondary mg-t-20" onclick="alarmQuitieren(\'' + bereich.ID + '\')">Alarm im Bereich <b>' + bereich.ID + '</b> quitieren</button><br><span id="alarmquitieren_' + bereich.ID + '"></span>';
          });
        } else {
          isAlarmequitierenButtonClicked = false
          for(let i = table.rows.length - 1; i >= 0; i--) {
            table.deleteRow(i);
          };
        }
      }

      async function alarmQuitieren(bereich) {
        const response = await fetch('/api/alarmquitieren?bereich=' + bereich);
        const responseobj = await response.json();
        if(response.status === 200) {
          let p = document.getElementById("alarmquitieren_" + bereich);
          p.innerHTML = '<span style="color: green; font-weight: bold;">' + responseobj.text + '</span>';
        } else {
          let p = document.getElementById("alarmquitieren_" + bereich);
          p.innerHTML = '<span style="color: red; font-weight: bold;">' + responseobj.text + '</span>';
        }

        //Die Tabelle in der Uebersicht aktuallisieren
        renewGetBereiche();

      }
