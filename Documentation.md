## Wichtige Klassen

- urls.py: Liste mit allen verfügbaren URL-Pattern. Sobald im Browser eine URL eingegeben wird, wird diese gesuchte URL mit den Regex-URL-Pattern in der urls.py verglichen. Ist das entsprechende Pattern vorhanden, wird die entsprechende View gerufen.
- views.py: Enthält alle verfügbaren Views. Zu jedem URL-Pattern in urls.py sollte eine View vorhanden sein. 
	- home_view: die Datei "installedHarvesters.txt" wird eingelesen um herauszufinden, welche Harvester installiert sind. Diese werden dann mit ihren verfügbaren Parametern auf der Homepage dargestellt. Wird das Formular vom User submitted, werden die angegebenen Parameter mit den verfügbaren Parametern für jeden Harvester gematched und der Harvester wird ausgeführt.
	- uploadHarvester_view: hier werden neue Harvester hochgeladen. Dazu werden die Methoden zum Installieren aus dem harvesterToolkit verwendet.
	- login/logout/password-view: alles erst mal nur Dummie-Views. Werden erst sinnvoll, sobald eine Datenbank im Hintergrund ist, über die die Nutzer dann tatsächlich verwaltet werden können.
- forms.py: Hier sind die Formulare für die uploadHarvester- und die Password-View implementiert.
- settings.py: enthält alle Django-Einstellungen. Enthält außerdem noch einige globale Variablen, die in views.py bzw. harvesterToolkit.py verwendet werden. Beispielsweise welche API-Parameter es gibt o.ä.
- harvesterToolkit.py: enthält alle möglichen Methoden, die zum hochladen/entpacken/ausführen der Harvester verwendet werden. Diese werden i.d.R. aus views.py gerufen.
- static/Harvesters: dieser Folder enthält alle installierten Harvester. Diese werden beim Upload hier her entpackt. Jeder in einem eigenen Folder. Außerdem liegt hier die "installedHarvesters.txt", die alle wichtigen Informationen über installierte Harvester enthält (Achtung: die Datei "installedHarvesters.txt" ist eine automatisiert generierte Datei und sollte nicht gelöscht werden).
- Templates-Folder: enthält für jede View ein Template, plus zusätzliche Templates wie z.B. das base_template, von dem die anderen Templates ableiten. 


## Konventionen

Die Config-Dateien sollten folgende Form haben:

```
	[Harvester]
	harvester_name = Facebook Harvester
	harvester_exe = facebookHarvester.py

	[Parameters]
	keyword = kw
	longitude = long
	area = area
	parameter1 = person
	parameter2 = likes

	[RelevantModules]
	module1 = someModule
	module2 = someOtherModule
```

Dabei haben die folgenden API-Parameter eine Sonderstellung: 

```
	keyword
	latitude
	longitude
	area
```

Diese werden wie oben ersichtlich in der Form

```
	keyword = kw
```

angegeben. Dabei entspricht "kw" dem Namen, den der Parameter "keyword" im hochgeladenen Harvester hat. Alle Parameter die nicht einem der oben genannten API-Parameter entsprechen werden einfach mit "paramter1" bis "parameterN" durchnummeriert. Analog ist die vorgehensweise bei den vom Harvester benötigten Python-Modulen. Die hier gelisteten Python-Module werden auf dem Server installiert. Eine exakte Nennung der Module ist daher wichtig.


----------


Beim Upload der Harvester befinden sich zwei Dateien in einem einfachen .zip-File ohne weitere Ordner o.ä.

Eine Datei entspricht der Konfigurationsdatei, die wie oben erläutert auszusehen hat. Die genaue Dateieindung spielt keine Rolle. Es sollte sich um eine einfache Textdatei handeln, die Endungen wie beispielsweise ".txt", ".cnf" oder ".config" haben könnte.

Die andere Datei sollte das Harvester-Script mit der Dateiendung ".py" sein. Beispielhafter Aufbau:

```
	- TwitterHarvester.zip
		- twitterHarvester.config
		- twitterHarvester.py 
```

Beim Upload der .zip-Datei ist zu beachten, dass der exakte Name der Konfigurationsdatei **inklusive** Dateiendung angegeben wird.
Außerdem sollten weder der Name des Harvesters, noch die Dateinamen Leer- oder Sonderzeichen enthalten.

## Noch nicht implementiert

- Datenbankandindung, vorzugsweise an eine NoSQL-DB
- besseres User-Feedback falls Fehler auftreten, insbesondere beim Upload der Harvester
- Tritt beim Upload ein Fehler auf, muss unter Umständen noch manuell aufgeräumt werden (z.B. zip-Datei wurde bereits entpackt, danach tritt ein Fehler auf -> entpackte Dateien müssen manuell gelöscht werden)
- Extra-Seite zum aktualisieren bereits im Framework installierter Harvester. Beispielsweise könnte es auf dieser Seite die Möglichkeit geben eine Konfigurationsdatei anzusehen, zu verändern oder eine neue hochzuladen. Das Gleiche am besten auch für die Python-Datei.
- Genaue Ansprüche an die Harvester-Skripte sind noch nicht klar. Hängt davon ab, wie genau die Harvester-Skripte vom Framework gerufen werden. Aktueller Ansatz: ein Bash-Kommando absetzen, dass die Skripte ausführt.** 

**Bei diesem Ansatz müssten die Harvester-Skripte sich ihre Parameter beispielsweise auf folgendem Wege holen, da die Parameter als Commandline-Argument übergeben werden:

```
	import sys
	argument1 = sys.argv[0]
	argument2 = sys.argv[1]
	etc.
```
