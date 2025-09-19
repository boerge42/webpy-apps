# Meine web.py-Apps

[web.py](https://webpy.org/) ist ein Web-Framework für Phyton, bei dem ein "10-Zeiler" ausreicht, 
um eine einfache Web-Seite, inclusive Webserver, an den Start zu bringen. Der Beitrag 
["Web.py - ein schlankes Web-Framework für Python"](https://www.linux-magazin.de/ausgaben/2006/08/die-zeit-laeuft/) im deutschen 
[Linux Magazin](https://www.linux-magazin.de/) [08/2006](https://www.linux-magazin.de/magazine/2006/08/) war, 
wenn auch erst Jahre später, für mich der Initialzünder, um sich mit diesem Thema zu beschäftigen und einige web.py-Applikationen zu schreiben.

Im Jahr 2022 habe ich auf der [FrOSCon](https://froscon.org/) und den [Chemnitzer Linux Tagen](https://chemnitzer.linux-tage.de) jeweils einen 
["Hello World"-Vortrag](webpy.pdf) zu [web.py](https://webpy.org/) gehalten. 

Folgendes ist in diesem Repository zu finden:

- [web_hello_world](https://github.com/boerge42/webpy-apps/tree/master/web_hello_world) &rarr; die Beispiele aus dem oben erwähnten 
["Hello World"-Vortrag](webpy.pdf) auf der/den [FrOSCon](https://froscon.org/)/[CLT](https://chemnitzer.linux-tage.de)

- [web_cd_search](https://github.com/boerge42/webpy-apps/tree/master/web_cd_search) &rarr; ein einfaches Web-Frontend, mit dem man über eine Datenbank 
(hier [MariaDB](https://mariadb.org/)), nach verschiedenen Kriterien (Album, Interpret, Titel, etc.), CDs suchen kann. Der Import der Daten erfolgt 
über ein [Python-Script](https://github.com/boerge42/webpy-apps/blob/master/web_cd_search/file_scan/mp3_scan.py), welches eine vorhandene mp3-Musiksammlung 
an Hand der vorhandenen [ID3-Tags](https://de.wikipedia.org/wiki/ID3-Tag) entsprechend analysiert/kategorisiert.

- [web_weather](https://github.com/boerge42/webpy-apps/tree/master/web_weather) &rarr; ... wenn denn mal die Aufzeichnung von Temperatur, Luftfeuchtigkeit, 
Luftdruck, etc. mit der "momentanen Hardware" funktioniert :-), werden hier die entsprechenden Diagramme, welche zyklisch aus den aufgenommen Daten via 
[gnuplot](http://gnuplot.info/) erzeugt werden, visualisiert.

- [web_smarthome](https://github.com/boerge42/webpy-apps/tree/master/web_smarthome) &rarr; jaja, 
[ich wollte nie Smarthome machen](https://programm.froscon.org/2021/events/2637.html)!; hier (trotzdem) eine Web-Applikation, mit der man (meine) Smarthome-Devices 
visualisieren/steuern könnte, wenn  die entsprechenden Voraussetzungen gegeben sind.

- [web_manfred](https://github.com/boerge42/webpy-apps/tree/master/web_manfred) &rarr; "Manfred" wollte auch sein CD-Inventar online durchsuchen können. 
Besonderheit ist hier, dass eine [csv-Datei](https://de.wikipedia.org/wiki/CSV_(Dateiformat) mit einem definierten/festgelegten Format, welche via 
Datei-Upload hochgeladen werden kann, nach diversen [Kriterien analysiert/geprüft](https://github.com/boerge42/webpy-apps/blob/master/web_manfred/manfred_upload.png) 
wird und dann entsprechend in eine interne Datenbank (hier [sqlite](https://sqlite.org/)) 
importiert wird.

---
Have fun!

Uwe Berger; 2022, 2024, 2025













